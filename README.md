# Draper AI Pitch Coach

AI-powered pitch deck review tool for Draper Associates that provides instant feedback on startup pitch decks.

> 📚 **For complete project documentation including current status and setup progress, see [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)**

## Quick Links

- **Live HF Space**: https://huggingface.co/spaces/displace-agency/draper-pitch-coach
- **Webflow Integration Guide**: [WEBFLOW_INTEGRATION.md](WEBFLOW_INTEGRATION.md)
- **Full Documentation**: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

## Features

- 🤖 GPT-4o powered analysis
- 📊 Structured feedback following VC best practices
- 🔒 Secure file handling and rate limiting
- 📝 Google Sheets logging
- ☁️ Google Drive storage
- 🌐 API endpoints for integration
- 🎨 Gradio UI for standalone use

## Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/displace-agency/draper-pitch-review.git
cd draper-pitch-review
```

### 2. Set Environment Variables
Required environment variables:
- `OPENAI_API_KEY`
- `FOLDER_ID` 
- `SHEET_ID`
- `GOOGLE_CREDENTIALS_JSON`
- `ALLOWED_ORIGINS`

### 3. Deploy to Hugging Face Space
1. Create new Space at https://huggingface.co/new-space
2. Select Gradio SDK
3. Link to this repository
4. Add environment variables in Settings

### 4. Integrate with Webflow
See [WEBFLOW_INTEGRATION.md](WEBFLOW_INTEGRATION.md) for detailed instructions.

## Current Status

**🔄 Configuration Phase** - The application is deployed but awaiting environment variables configuration.

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md#current-status) for detailed status.

## API Usage

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

## Project Structure

```
draper-pitch-review/
├── app.py                      # Main application with Gradio UI and API
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── Logo.png                    # Draper logo
├── README.md                   # This file
├── PROJECT_DOCUMENTATION.md    # Complete project documentation
├── WEBFLOW_INTEGRATION.md      # Webflow integration guide
├── .gitignore                  # Git ignore rules
└── .gitattributes             # Git LFS configuration
```

## Support

For questions or issues:
- Create a GitHub issue
- Contact: hello@displace.agency
- See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md#contact--support)

---

Built for [Draper Associates](https://www.draper.vc) by [Displace Agency](https://displace.agency)
