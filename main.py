from fastapi import FastAPI
import os
import smtplib
from email.message import EmailMessage

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "NeuroX is live and connected."}

@app.get("/test-email")
def send_test_email():
    email_address = os.getenv("NOTIFY_EMAIL")
    email_password = os.getenv("GMAIL_TOKEN")

    msg = EmailMessage()
    msg['Subject'] = 'Test from NeuroX'
    msg['From'] = email_address
    msg['To'] = email_address
    msg.set_content("✅ This is a test email from NeuroX — your system works!")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

    return {"message": "📬 Test email sent successfully!"}
