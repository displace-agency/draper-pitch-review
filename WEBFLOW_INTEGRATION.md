# Webflow Integration Guide

## API Endpoints

The Draper Pitch Review tool provides the following API endpoints for integration with Webflow:

### 1. Create Session
**POST** `/api/create-session`

Creates a session token for multi-step form validation.

**Request Body:**
```json
{
  "name": "Founder Name",
  "email": "founder@example.com", 
  "company": "Startup Name",
  "form_step": 7
}
```

**Response:**
```json
{
  "session_token": "abc123..."
}
```

### 2. Analyze Pitch
**POST** `/api/analyze-pitch`

Analyzes the pitch deck and returns AI feedback.

**Request:** 
- Content-Type: `multipart/form-data`
- Fields:
  - `file`: PDF file (max 10MB)
  - `name`: Founder name
  - `email`: Email address
  - `session_token`: (optional) Session token from create-session

**Response:**
```json
{
  "status": "success",
  "feedback": "Full AI feedback text...",
  "logged": true
}
```

## Webflow Integration Code

Add this to your Webflow custom code:

```javascript
// Configuration
const API_BASE_URL = 'https://your-space.hf.space';
let sessionToken = null;

// Create session when form starts
async function createSession(formData) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/create-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        name: formData.name,
        email: formData.email,
        company: formData.company,
        form_step: formData.currentStep
      })
    });
    
    const data = await response.json();
    sessionToken = data.session_token;
    return sessionToken;
  } catch (error) {
    console.error('Session creation failed:', error);
    return null;
  }
}

// Analyze pitch deck
async function analyzePitch(file, name, email) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('name', name);
  formData.append('email', email);
  if (sessionToken) {
    formData.append('session_token', sessionToken);
  }

  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze-pitch`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Analysis failed');
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Pitch analysis failed:', error);
    throw error;
  }
}

// Integration with Webflow form
document.addEventListener('DOMContentLoaded', function() {
  // Hook into your multi-step form
  const form = document.querySelector('[data-form="multi-step"]');
  
  // Create session on first step completion
  form.addEventListener('step-complete', async (e) => {
    if (e.detail.step === 1) {
      await createSession({
        name: form.querySelector('[name="founder-name"]').value,
        email: form.querySelector('[name="email"]').value,
        company: form.querySelector('[name="startup-name"]').value,
        currentStep: e.detail.step
      });
    }
  });
  
  // Add review step after deck upload
  const fileInput = document.querySelector('[name="pitch-deck"]');
  const reviewButton = document.createElement('button');
  reviewButton.textContent = 'Get AI Feedback';
  reviewButton.className = 'button is-form';
  reviewButton.style.display = 'none';
  
  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) {
      reviewButton.style.display = 'block';
    }
  });
  
  reviewButton.addEventListener('click', async (e) => {
    e.preventDefault();
    
    // Show loading state
    reviewButton.disabled = true;
    reviewButton.textContent = 'Analyzing...';
    
    try {
      const result = await analyzePitch(
        fileInput.files[0],
        form.querySelector('[name="founder-name"]').value,
        form.querySelector('[name="email"]').value
      );
      
      // Display feedback
      displayFeedback(result.feedback);
      
      // Enable continue button
      document.querySelector('[data-form="next-btn"]').disabled = false;
      
    } catch (error) {
      alert('Analysis failed: ' + error.message);
      reviewButton.disabled = false;
      reviewButton.textContent = 'Try Again';
    }
  });
  
  // Insert review button after file input
  fileInput.parentNode.appendChild(reviewButton);
});

// Display feedback in modal or inline
function displayFeedback(feedback) {
  const modal = document.createElement('div');
  modal.className = 'feedback-modal';
  modal.innerHTML = `
    <div class="feedback-content">
      <h3>AI Pitch Feedback</h3>
      <div class="feedback-text">${feedback.replace(/\n/g, '<br>')}</div>
      <button onclick="this.parentElement.parentElement.remove()">Close</button>
    </div>
  `;
  document.body.appendChild(modal);
}
```

## Environment Variables

Set these in your Hugging Face Space settings:

- `OPENAI_API_KEY`: Your OpenAI API key
- `FOLDER_ID`: Google Drive folder ID for storing PDFs
- `SHEET_ID`: Google Sheets ID for logging submissions
- `GOOGLE_CREDENTIALS_JSON`: Google service account credentials as JSON string
- `ALLOWED_ORIGINS`: Comma-separated list of allowed domains (e.g., "https://draper-vc.design.webflow.com,https://www.draper.vc")
- `OPENAI_PROMPT`: Custom prompt for GPT-4o analysis

## Security Considerations

1. **Rate Limiting**: 3 submissions per email per 24 hours
2. **File Validation**: PDF only, max 10MB
3. **CORS**: Only allowed origins can access the API
4. **Session Validation**: Optional session tokens for form continuity
5. **Input Sanitization**: Email validation and text sanitization

## Testing

1. Test CORS by making a request from your Webflow domain
2. Verify file upload limits
3. Test rate limiting with multiple submissions
4. Check error handling for various scenarios

## Support

For issues or questions, contact: hello@displace.agency
