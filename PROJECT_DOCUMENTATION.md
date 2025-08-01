# Draper AI Pitch Coach - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture & Components](#architecture--components)
3. [Accounts & Services](#accounts--services)
4. [Current Status](#current-status)
5. [Setup Progress](#setup-progress)
6. [Remaining Tasks](#remaining-tasks)
7. [Integration Details](#integration-details)
8. [Technical Implementation](#technical-implementation)
9. [Security Measures](#security-measures)
10. [Troubleshooting](#troubleshooting)

## Project Overview

### Purpose
The Draper AI Pitch Coach is an AI-powered tool designed to integrate into Draper Associates' website contact form. It provides instant, constructive feedback on startup pitch decks before final submission, helping founders improve their pitches while saving time for the investment team.

### Key Features
- **Pre-submission Review**: Founders get AI feedback before submitting their pitch
- **GPT-4o Analysis**: Structured feedback following VC best practices
- **Secure Processing**: Rate limiting, file validation, and session management
- **Data Logging**: All submissions logged to Google Sheets with PDFs stored in Google Drive
- **Webflow Integration**: Seamlessly embedded in the existing multi-step contact form

### User Flow
1. Founder fills out multi-step form on Draper website
2. Uploads pitch deck (PDF) at step 7
3. Clicks "Get AI Feedback" button
4. Receives instant analysis with structured feedback
5. Can update deck based on feedback
6. Proceeds to final submission

## Architecture & Components

### System Architecture
```
Webflow Contact Form
    ↓
Hugging Face Space (API)
    ↓
┌─────────────┬──────────────┬─────────────────┐
│  OpenAI API │ Google Drive │ Google Sheets   │
│  (GPT-4o)   │ (PDF Storage)│ (Logging)       │
└─────────────┴──────────────┴─────────────────┘
```

### Technology Stack
- **Frontend**: Webflow (existing Draper website)
- **Backend**: Hugging Face Spaces (Python/Gradio/FastAPI)
- **AI**: OpenAI GPT-4o
- **Storage**: Google Drive (PDFs), Google Sheets (metadata)
- **Languages**: Python, JavaScript
- **Frameworks**: Gradio, FastAPI, CORS middleware

## Accounts & Services

### 1. GitHub Repository
- **URL**: https://github.com/displace-agency/draper-pitch-review
- **Owner**: displace-agency
- **Purpose**: Source code management
- **Status**: ✅ Created and populated with all code

### 2. Hugging Face Space
- **URL**: https://huggingface.co/spaces/displace-agency/draper-pitch-coach
- **Owner**: displace-agency
- **Purpose**: Hosts the API and Gradio interface
- **Status**: ✅ Created, code uploaded, ⚠️ awaiting environment variables

### 3. Google Cloud Services
- **Google Drive Folder**: https://drive.google.com/drive/folders/1qvDHxWt17BfQbobYoxk5MCGVD8315HNN
  - **Folder ID**: `1qvDHxWt17BfQbobYoxk5MCGVD8315HNN`
  - **Purpose**: Store uploaded pitch deck PDFs
  
- **Google Sheet**: https://docs.google.com/spreadsheets/d/1Fa0fTBKfGMSiYtNsLC-f3rqim9JsGnyWP-XGUSvXvEg/
  - **Sheet ID**: `1Fa0fTBKfGMSiYtNsLC-f3rqim9JsGnyWP-XGUSvXvEg`
  - **Purpose**: Log submissions (timestamp, name, email, PDF link, AI feedback)
  
- **Service Account**: ❌ Needs to be created
  - **Purpose**: Authenticate API access to Drive/Sheets

### 4. OpenAI Account
- **API Key**: ❌ Needs to be added to HF Space
- **Model**: GPT-4o
- **Purpose**: Generate pitch deck analysis

### 5. Webflow Site
- **Contact Page**: https://draper-vc.design.webflow.com/?locale=en&pageId=685e213f391b5e21bae07a12
- **Live Site**: https://www.draper.vc/contact
- **Status**: ⚠️ Awaiting integration code

## Current Status

### ✅ Completed
1. **Source Code Development**
   - Enhanced `app.py` with API endpoints and security
   - Created `config.py` for environment-based configuration
   - Added comprehensive `requirements.txt`
   - Documentation files (README, WEBFLOW_INTEGRATION)

2. **Repository Setup**
   - GitHub repository created and populated
   - All files uploaded including .gitattributes and .gitignore
   - Comprehensive documentation added

3. **Hugging Face Space**
   - Space created: draper-pitch-coach
   - All files uploaded from GitHub
   - Currently showing configuration error (expected - needs env vars)

### ⚠️ In Progress
1. **Environment Variables Configuration**
   - Need to add secrets to HF Space settings
   - Waiting for Google Cloud credentials

2. **Google Cloud Setup**
   - Need to create service account
   - Enable Drive and Sheets APIs
   - Generate credentials JSON

### ❌ Not Started
1. **Webflow Integration**
   - Add JavaScript code to contact form
   - Test API connectivity
   - Style feedback display

2. **Testing & Deployment**
   - End-to-end testing
   - Security validation
   - Performance optimization

## Setup Progress

### Step-by-Step Progress Tracker

#### Phase 1: Infrastructure Setup ✅
- [x] Clone original HF Space from bkifle
- [x] Create GitHub repository
- [x] Remove sensitive credentials
- [x] Push code to GitHub
- [x] Create new HF Space
- [x] Upload code to HF Space

#### Phase 2: Configuration 🔄
- [ ] Create Google Cloud Project
- [ ] Enable Google APIs (Drive, Sheets)
- [ ] Create Service Account
- [ ] Download credentials JSON
- [ ] Share Drive folder with service account
- [ ] Share Google Sheet with service account
- [ ] Add environment variables to HF Space:
  - [ ] OPENAI_API_KEY
  - [ ] FOLDER_ID ✅ (have value: `1qvDHxWt17BfQbobYoxk5MCGVD8315HNN`)
  - [ ] SHEET_ID ✅ (have value: `1Fa0fTBKfGMSiYtNsLC-f3rqim9JsGnyWP-XGUSvXvEg`)
  - [ ] GOOGLE_CREDENTIALS_JSON
  - [ ] ALLOWED_ORIGINS
  - [ ] OPENAI_PROMPT (optional)

#### Phase 3: Integration 📝
- [ ] Test HF Space is working
- [ ] Add integration code to Webflow
- [ ] Test API endpoints
- [ ] Style feedback display
- [ ] Add loading states

#### Phase 4: Testing & Launch 🚀
- [ ] Test rate limiting
- [ ] Test file validation
- [ ] Test error handling
- [ ] Performance testing
- [ ] Security review
- [ ] Go live

## Remaining Tasks

### Immediate Next Steps (Today)

1. **Google Cloud Setup** (30 minutes)
   ```
   1. Go to https://console.cloud.google.com
   2. Create new project "draper-pitch-coach"
   3. Enable APIs: Google Drive API, Google Sheets API
   4. Create service account
   5. Download JSON credentials
   6. Share Drive/Sheets with service account email
   ```

2. **Configure HF Space** (10 minutes)
   ```
   1. Go to HF Space Settings
   2. Add Repository secrets:
      - OPENAI_API_KEY: [your key]
      - FOLDER_ID: 1qvDHxWt17BfQbobYoxk5MCGVD8315HNN
      - SHEET_ID: 1Fa0fTBKfGMSiYtNsLC-f3rqim9JsGnyWP-XGUSvXvEg
      - GOOGLE_CREDENTIALS_JSON: [your JSON on one line]
      - ALLOWED_ORIGINS: https://draper-vc.design.webflow.com,https://www.draper.vc
   ```

3. **Test API** (15 minutes)
   - Verify Space is running
   - Test with sample PDF
   - Check Google Drive/Sheets integration

### Tomorrow's Tasks

1. **Webflow Integration**
   - Add JavaScript code from WEBFLOW_INTEGRATION.md
   - Modify form step progression
   - Add feedback display UI
   - Test in Webflow preview

2. **Final Testing**
   - Complete user flow test
   - Security validation
   - Performance check

## Integration Details

### Webflow Form Structure
The contact form at `/contact` has these steps:
1. Founder & Startup Info
2. What Are You Building?
3. Traction & Metrics
4. Fundraising
5. Team
6. Market & Competition
7. **The Deck** (PDF upload) ← Integration point
8. **[NEW] AI Review** ← To be added
9. Final Submission

### API Endpoints

#### 1. Create Session
```
POST https://displace-agency-draper-pitch-coach.hf.space/api/create-session
Content-Type: application/x-www-form-urlencoded

name=John+Doe&email=john@startup.com&company=MyStartup&form_step=7
```

#### 2. Analyze Pitch
```
POST https://displace-agency-draper-pitch-coach.hf.space/api/analyze-pitch
Content-Type: multipart/form-data

file=@pitch.pdf&name=John+Doe&email=john@startup.com&session_token=abc123
```

### JavaScript Integration Code
See `WEBFLOW_INTEGRATION.md` for complete code. Key parts:
- Session creation on form start
- File upload handling
- API call on "Get AI Feedback" button
- Feedback display in modal/inline
- Error handling

## Technical Implementation

### Security Features
1. **Rate Limiting**: 3 submissions per email per 24 hours
2. **File Validation**: PDF only, max 10MB
3. **CORS Protection**: Only allowed domains
4. **Session Management**: Token-based validation
5. **Input Sanitization**: Email validation, XSS prevention

### Data Flow
1. User uploads PDF → Validated locally
2. API call with file + metadata
3. PDF extracted (text + images)
4. GPT-4o analysis with custom prompt
5. PDF saved to Google Drive
6. Metadata + feedback logged to Sheets
7. Response returned to user

### Error Handling
- Invalid file format → Clear error message
- Rate limit exceeded → 24-hour cooldown notice
- API failures → Graceful degradation
- Network issues → Retry mechanism

## Security Measures

### Implemented
- Environment variables for sensitive data
- CORS middleware with allowed origins
- File type and size validation
- Email format validation
- Rate limiting by email
- Session token validation

### Best Practices
- No credentials in code
- HTTPS only communication
- Temporary file cleanup
- Audit logging
- Error message sanitization

## Troubleshooting

### Common Issues

1. **"Configuration Error" in HF Space**
   - **Cause**: Missing environment variables
   - **Fix**: Add all required secrets in Settings

2. **"Failed to get Google credentials"**
   - **Cause**: Invalid or missing GOOGLE_CREDENTIALS_JSON
   - **Fix**: Ensure JSON is valid and on one line

3. **CORS Errors from Webflow**
   - **Cause**: Domain not in ALLOWED_ORIGINS
   - **Fix**: Add domain to environment variable

4. **Rate Limit Errors**
   - **Cause**: User exceeded 3 submissions in 24 hours
   - **Fix**: Wait or use different email

### Debug Checklist
- [ ] Check HF Space logs
- [ ] Verify environment variables set
- [ ] Test with Gradio UI first
- [ ] Check browser console for JS errors
- [ ] Verify API endpoints accessible
- [ ] Check Google Drive/Sheets permissions

## Contact & Support

**Project Owner**: Displace Agency
- Email: hello@displace.agency
- GitHub: @displace-agency

**Original Tool Creator**: @bkifle (Hugging Face)

**For Draper Team**:
- Integration support: Contact Displace Agency
- API keys/credentials: Contact your IT admin
- Feature requests: Create GitHub issue

---

**Last Updated**: August 1, 2025
**Version**: 1.0.0
**Status**: In Development - Configuration Phase
