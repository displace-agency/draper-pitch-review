import json
import os
from google.oauth2.service_account import Credentials

def get_google_credentials():
    """Get Google credentials from environment variable or file"""
    # First try to get from environment variable (for production)
    google_creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    
    if google_creds_json:
        try:
            creds_dict = json.loads(google_creds_json)
            scopes = [
                'https://www.googleapis.com/auth/drive',
                'https://www.googleapis.com/auth/spreadsheets'
            ]
            return Credentials.from_service_account_info(creds_dict, scopes=scopes)
        except Exception as e:
            print(f"Error parsing Google credentials from env: {e}")
    
    # Fallback to file if it exists (for local development)
    if os.path.exists('creds.json'):
        scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        return Credentials.from_service_account_file('creds.json', scopes=scopes)
    
    raise ValueError("No Google credentials found. Set GOOGLE_CREDENTIALS_JSON environment variable.")

def get_allowed_origins():
    """Get allowed origins for CORS"""
    origins = os.getenv("ALLOWED_ORIGINS", "https://draper-vc.design.webflow.com,https://www.draper.vc").split(",")
    return [origin.strip() for origin in origins]
