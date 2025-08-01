import gradio as gr
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
from openai import OpenAI
import os
import base64
import datetime
import gspread
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import re
import tempfile
import uvicorn
from typing import Optional
import hashlib
import json
from config import get_google_credentials, get_allowed_origins

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Session storage (in production, use Redis or similar)
session_store = {}

def create_session_token(email: str, form_data: dict) -> str:
    """Create a session token for form validation"""
    data = f"{email}{form_data}{datetime.utcnow().isoformat()}"
    return hashlib.sha256(data.encode()).hexdigest()

def validate_session(token: str) -> bool:
    """Validate session token"""
    # In production, check against Redis/database
    return token in session_store and session_store[token]['expires'] > datetime.utcnow()

def is_valid_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email)

def is_email_limited(email, sheet):
    now = datetime.utcnow()
    past_24hrs = now - timedelta(days=1)
    records = sheet.get_all_records()
    recent_submissions = [
        row for row in records
        if row.get("Email") == email and
        datetime.fromisoformat(row.get("Timestamp")) > past_24hrs
    ]
    return len(recent_submissions) >= 3

def log_to_google(name, email, file_path, file_name, gpt_feedback):
    print("📤 Logging submission to Google Drive...")
    
    try:
        creds = get_google_credentials()
    except Exception as e:
        print(f"❌ Failed to get Google credentials: {e}")
        return False, "Error with Google credentials"

    # Upload to Drive
    drive_service = build('drive', 'v3', credentials=creds)
    folder_id = os.getenv("FOLDER_ID")
    print(f"📁 Using folder ID: {folder_id}")

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(file_path, mimetype='application/pdf')
    
    try:
        uploaded = drive_service.files().create(
            body=file_metadata, media_body=media, fields='id', supportsAllDrives=True
        ).execute()
        print(f"✅ File uploaded with ID: {uploaded['id']}")
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return False, "Error uploading file"

    file_id = uploaded['id']
    link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    print(f"🔗 File link: {link}")

    try:
        gc = gspread.authorize(creds)
        sheet_id = os.getenv("SHEET_ID")
        sheet = gc.open_by_key(sheet_id).sheet1
            
        sheet.append_row([
            datetime.utcnow().isoformat(),
            name,
            email,
            link,
            gpt_feedback
        ])
        print("📈 Logged submission to Google Sheet.")
        return True, "Logged successfully"
    except Exception as e:
        print(f"❌ Error logging to sheet: {e}")
        return False, "Error logging to sheet"

def extract_text_from_pdf(pdf_file_path):
    print("📄 Extracting text from PDF...")
    with fitz.open(pdf_file_path) as doc:
        return "\n".join([page.get_text() for page in doc])

def extract_images_from_pdf(pdf_file_path):
    print("🖼️ Extracting images from PDF...")
    images = []
    with fitz.open(pdf_file_path) as doc:
        for page in doc:
            pix = page.get_pixmap(dpi=150)
            img_bytes = pix.tobytes("png")
            b64_img = base64.b64encode(img_bytes).decode("utf-8")
            images.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}})
    return images

def generate_feedback(deck_text=None, image_payload=None):
    print("🤖 Generating feedback with GPT...")
    base_text = os.getenv("OPENAI_PROMPT", """
    You are a Draper Associates venture analyst reviewing a pitch deck. Provide feedback following this structure:

    1. Summary of the Startup
    2. Strengths
    3. Areas for Improvement
    4. Missing or Underexplained Topics
    5. Strategic Fit with Draper
    6. 2-3 Actionable Suggestions
    7. Optional Pushback or Contrarian Take

    Be constructive, specific, and actionable. Focus on helping the founder improve their pitch.
    """)
    
    content_block = [{"type": "text", "text": base_text}]

    if deck_text:
        content_block.append({"type": "text", "text": f"---\nPitch Deck Content:\n{deck_text}"})
    if image_payload:
        content_block.extend(image_payload)

    messages = [
        {"role": "system", "content": "You are a Draper Associates venture analyst reviewing a pitch deck."},
        {"role": "user", "content": content_block}
    ]

    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.7,
        stream=True
    )

    accumulated_output = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content or ""
        accumulated_output += delta
        yield accumulated_output

def validate_inputs(name, email, file_path=None):
    print("🔍 Validating inputs...")
    if not name.strip() or not email.strip():
        print("❌ Missing name or email.")
        return False, "❌ Name and email are required."
    
    if not is_valid_email(email):
        return False, "❌ Please enter a valid email address."
    
    if file_path:
        if not file_path.lower().endswith(".pdf"):
            print("❌ Invalid file format.")
            return False, "❌ Please upload a PDF file."
        
        try:
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:  # 10 MB
                print("❌ File too large.")
                return False, "❌ File too large. Max 10MB."
        except Exception as e:
            print(f"❌ Error checking file size: {e}")
            return False, "❌ Error validating file."

    return True, ""

# API Endpoints
@app.post("/api/create-session")
async def create_session(
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(...),
    form_step: int = Form(...)
):
    """Create a session for the multi-step form"""
    is_valid, msg = validate_inputs(name, email)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    token = create_session_token(email, {"name": name, "company": company})
    session_store[token] = {
        "email": email,
        "name": name,
        "company": company,
        "form_step": form_step,
        "expires": datetime.utcnow() + timedelta(hours=1)
    }
    
    return JSONResponse({"session_token": token})

@app.post("/api/analyze-pitch")
async def analyze_pitch_api(
    file: UploadFile = File(...),
    name: str = Form(...),
    email: str = Form(...),
    session_token: Optional[str] = Form(None)
):
    """API endpoint for pitch analysis"""
    # Validate session if provided
    if session_token and not validate_session(session_token):
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    # Validate inputs
    is_valid, msg = validate_inputs(name, email)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        # Check submission quota
        creds = get_google_credentials()
        gc = gspread.authorize(creds)
        sheet_id = os.getenv("SHEET_ID")
        sheet = gc.open_by_key(sheet_id).sheet1
        
        if is_email_limited(email, sheet):
            os.unlink(tmp_file_path)
            raise HTTPException(
                status_code=429, 
                detail="You've reached the limit of 3 submissions in the last 24 hours."
            )
        
        # Extract content
        text = extract_text_from_pdf(tmp_file_path)
        image_payload = extract_images_from_pdf(tmp_file_path)
        
        if not text.strip() and not image_payload:
            os.unlink(tmp_file_path)
            raise HTTPException(status_code=400, detail="No extractable content found in PDF")
        
        # Generate feedback
        full_feedback = ""
        for partial_output in generate_feedback(
            deck_text=text if text.strip() else None, 
            image_payload=image_payload
        ):
            full_feedback = partial_output
        
        # Log to Google
        success, log_msg = log_to_google(name, email, tmp_file_path, file.filename, full_feedback)
        
        # Clean up
        os.unlink(tmp_file_path)
        
        return JSONResponse({
            "status": "success",
            "feedback": full_feedback,
            "logged": success
        })
        
    except Exception as e:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

# Gradio interface functions (unchanged)
def analyze_pitch_gradio(file, name, email, human_check):
    print(f"📥 New submission: {name} | {email} | {file.name}")
    is_valid, msg = validate_inputs(name, email, file.name)
    if not is_valid:
        yield msg
        return

    # Check submission quota early
    try:
        creds = get_google_credentials()
        gc = gspread.authorize(creds)
        sheet_id = os.getenv("SHEET_ID")
        sheet = gc.open_by_key(sheet_id).sheet1

        if is_email_limited(email, sheet):
            print("⛔ Email has exceeded daily submission limit.")
            yield "❌ You've reached the limit of 3 submissions in the last 24 hours."
            return
    except Exception as e:
        print(f"❌ Failed to validate email limit: {e}")
        yield "❌ Internal error checking submission quota."
        return

    yield "📥 Request received. Extracting pitch content..."
    
    if not human_check:
        yield "❌ Please confirm you're not a robot."
        return
        
    try:
        text = extract_text_from_pdf(file.name)
        image_payload = extract_images_from_pdf(file.name)
    except Exception as e:
        print(f"❌ PDF Extraction error: {e}")
        yield "❌ Failed to read the pitch deck. Please ensure it's a valid PDF."
        return

    if not text.strip() and not image_payload:
        print("⚠️ No text or images found in the PDF.")
        yield "❌ No extractable text or slide images found."
        return

    yield "🧠 Analyzing pitch deck with Draper-GPT..."
    full_feedback = ""

    try:
        for partial_output in generate_feedback(deck_text=text if text.strip() else None, image_payload=image_payload):
            full_feedback = partial_output
            yield partial_output
    except Exception as e:
        print(f"❌ GPT Error: {e}")
        yield "❌ GPT analysis failed. Please try again later."
        return

    try:
        success, log_msg = log_to_google(name, email, file.name, file.name, full_feedback)
        if not success:
            yield log_msg

    except Exception as e:
        print(f"⚠️ Failed to log to Google: {e}")

# Gradio UI
with gr.Blocks(css=".gr-block { padding: 12px; display: flex; justify-content: center; }") as demo:
    with gr.Column(elem_id="centered-ui"):
        gr.Image(value="Logo.png", width=120, show_label=False, show_download_button=False)
        gr.Markdown("## PitchLens — Your AI Pitch Coach from Draper Associates")
        disclaimer_output = gr.Markdown(
            """
        ---
        _**Disclaimer:** The feedback provided through this tool is generated by AI (GPT-4o) and may contain inaccuracies or hallucinated content. It is intended for informational and preparatory purposes only and **does not constitute investment advice, a funding decision, or an indication of investment interest** from Draper Associates._
        
        _By submitting your pitch deck and contact information, you agree that your submission (including name, email, deck contents, and generated feedback) may be accessed and reviewed by the Draper Associates team. Data submitted may be used to help improve our processes and tools._  
        We're excited to learn more about your company!
        """
        )

        name_input = gr.Text(label="👤 Your Name")
        email_input = gr.Text(label="📧 Your Email")
        file_input = gr.File(label="📤 Upload your pitch deck (PDF)", file_types=[".pdf"])
        captcha = gr.Checkbox(label="✅ I am not a robot", value=False)

        submit_btn = gr.Button("Analyze Deck")

        feedback_output = gr.Markdown()
        disclaimer_output = gr.Markdown("---\n\n_This feedback is based solely on your submitted pitch deck. We have not seen a demo, spoken to your team, or reviewed outside information. Our goal is to help you sharpen your fundraising narrative through the lens of what early-stage investors like Draper Associates look for. This is not a funding decision or an investment signal._")

        submit_btn.click(fn=analyze_pitch_gradio,
                 inputs=[file_input, name_input, email_input, captcha],
                 outputs=feedback_output)

        gr.Markdown("---\n_Made by [Draper Associates](https://www.draper.vc) — powered by GPT-4o. Learn more about our fund, our mission, and how we back bold founders._")

# Mount Gradio app to FastAPI
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    # Run with: python app.py
    # This will serve both the Gradio UI and the API
    uvicorn.run(app, host="0.0.0.0", port=7860)
