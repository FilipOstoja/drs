import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import os

def send_email(recipient_email: str, subject: str, body: str, attachment_path: str):
    try:
        # Kreiranje SMTP servera (koristimo Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("TVOJMAIL@gmail.com", "sifra")  # Zamijenite s vašim e-mailom i app passwordom
        
        # Kreirajte MIME objekt
        msg = MIMEMultipart()
        msg['From'] = formataddr(('Filip Ostojic', 'mmmmailtvoj@gmailc.om'))  # Zamijenite sa svojim emailom
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Dodajte tijelo e-maila
        msg.attach(MIMEText(body, 'plain'))

        # Dodajte privitak (ako postoji)
        if attachment_path:
            filename = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)

        # Slanje e-maila
        server.sendmail("your_email@gmail.com", recipient_email, msg.as_string())
        server.quit()

        print(f"Email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")
