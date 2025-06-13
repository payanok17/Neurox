from fastapi import FastAPI
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "NeuroX is live and connected."}

@app.get("/test-email")
def send_test_email():
    sender_email = os.getenv("NOTIFY_EMAIL")
    sender_password = os.getenv("GMAIL_APP_TOKEN")
    receiver_email = os.getenv("NOTIFY_EMAIL")

    if not sender_email or not sender_password:
        return {"error": "Missing Gmail credentials. Check .env setup."}

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "✅ NeuroX Mail Bridge Test"
    msg.attach(MIMEText("This is a test email from your NeuroX system 🔗", "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return {"message": "📬 Test email sent successfully!"}
    except Exception as e:
        return {"error": f"Failed to send email: {str(e)}"}
