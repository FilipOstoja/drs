import smtplib

SMTP_SERVER = "smtp.example.com"
SMTP_PORT = 587
SMTP_USERNAME = "admin"
SMTP_PASSWORD = "admin"

def send_email(to_email: str, subject: str, message: str):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(SMTP_USERNAME, to_email, email_message)

    return {"status": "Email sent", "to": to_email}
