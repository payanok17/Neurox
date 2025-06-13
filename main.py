from fastapi import FastAPI
from starlette.responses import JSONResponse
import os
import requests
import base64

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "NeuroX is live and connected."}

@app.get("/test_email")
def test_email():
    access_token = os.getenv("GMAIL_ACCESS_TOKEN")
    to_email = os.getenv("NOTIFY_EMAIL")

    message = f"To: {to_email}\r\nSubject: NeuroX Alert\r\n\r\nTest email from NeuroX."
    encoded_message = base64.urlsafe_b64encode(message.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "raw": encoded_message
    }

    r = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers=headers,
        json=body
    )

    if r.status_code in [200, 202]:
        return {"status": "Email sent successfully"}
    else:
        return JSONResponse(status_code=r.status_code, content=r.json())
