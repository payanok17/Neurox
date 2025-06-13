from fastapi import FastAPI
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "NeuroX is live and connected."}

@app.get("/test-email")
def send_test_email():
    sender_email = os.getenv("NOTIFY_EMAIL")
    receiver_email = os.getenv("NOTIFY_EMAIL")
    
    client_id = os.getenv("GMAIL_CLIENT_ID")
    client_secret = os.getenv("GMAIL_CLIENT_SECRET")
    refresh_token = os.getenv("GMAIL_REFRESH_TOKEN")

    if not (client_id and client_secret and refresh_token and sender_email):
        return {"error": "Missing Gmail OAuth credentials. Check .env setup."}

    try:
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret
        )
        creds.refresh(Request())

        service = build('gmail', 'v1', credentials=creds)

        msg = MIMEMultipart()
        msg['To'] = receiver_email
        msg['From'] = sender_email
        msg['Subject'] = "✅ NeuroX Alert Test via Gmail API"
        msg.attach(MIMEText("This is a test email sent using OAuth and Gmail API", 'plain'))

        raw_msg = {'raw': msg.as_string().encode("utf-8").decode("latin1")}

        service.users().messages().send(userId="me", body=raw_msg).execute()
        return {"message": "📬 Gmail API alert sent successfully!"}

    except Exception as e:
        return {"error": f"Failed to send via Gmail API: {str(e)}"}
