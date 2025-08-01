# Draper AI Pitch Coach

AI-powered pitch deck review tool for Draper Associates that provides instant feedback on startup pitch decks.

## Features

- 🤖 GPT-4o powered analysis
- 📊 Structured feedback following VC best practices
- 🔒 Secure file handling and rate limiting
- 📝 Google Sheets logging
- ☁️ Google Drive storage
- 🌐 API endpoints for integration
- 🎨 Gradio UI for standalone use

## Setup

### 1. Create a Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Name your space (e.g., `draper-pitch-coach`)
3. Select "Gradio" as the SDK
4. Link to this GitHub repository

### 2. Configure Environment Variables

In your Hugging Face Space settings, add:

- `OPENAI_API_KEY`: Your OpenAI API key
- `FOLDER_ID`: Google Drive folder ID for PDF storage
- `SHEET_ID`: Google Sheets ID for logging
- `GOOGLE_CREDENTIALS_JSON`: Google service account credentials (JSON string)
- `ALLOWED_ORIGINS`: Allowed domains for CORS (comma-separated)
- `OPENAI_PROMPT`: Custom analysis prompt (optional)

### 3. Google Cloud Setup

1. Create a service account in Google Cloud Console
2. Enable Google Drive and Sheets APIs
3. Share your Drive folder and Sheet with the service account email
4. Download credentials and set as `GOOGLE_CREDENTIALS_JSON`

## API Usage

The tool provides REST API endpoints for integration:

### Create Session
```bash
POST /api/create-session
Content-Type: application/x-www-form-urlencoded

name=John+Doe&email=john@startup.com&company=MyStartup&form_step=7
```

### Analyze Pitch
```bash
POST /api/analyze-pitch
Content-Type: multipart/form-data

file=@pitch.pdf&name=John+Doe&email=john@startup.com&session_token=abc123
```

## Webflow Integration

See [WEBFLOW_INTEGRATION.md](WEBFLOW_INTEGRATION.md) for detailed integration instructions.

## Security Features

- Rate limiting: 3 submissions per email per 24 hours
- File validation: PDF only, max 10MB
- CORS protection
- Input sanitization
- Session validation

## Development

### Local Setup
```bash
# Clone the repository
git clone https://github.com/displace-agency/draper-pitch-review.git
cd draper-pitch-review

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-key"
export FOLDER_ID="your-folder-id"
export SHEET_ID="your-sheet-id"
export GOOGLE_CREDENTIALS_JSON='{"type":"service_account",...}'

# Run the app
python app.py
```

### Testing
- Access Gradio UI at http://localhost:7860
- Test API at http://localhost:7860/api/analyze-pitch

## Architecture

- **Frontend**: Gradio for UI, FastAPI for API endpoints
- **AI**: OpenAI GPT-4o for pitch analysis
- **Storage**: Google Drive for PDFs, Google Sheets for metadata
- **Security**: Rate limiting, CORS, input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions or issues:
- Create a GitHub issue
- Contact: hello@displace.agency

---

Built for [Draper Associates](https://www.draper.vc) by [Displace Agency](https://displace.agency)
