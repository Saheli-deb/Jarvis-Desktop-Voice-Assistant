import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# --- Clear Setup Instructions ---
SETUP_INSTRUCTIONS = '''
=== GMAIL EMAIL SETUP ===

You need to add your Gmail credentials to a .env file.

STEP 1: Choose your method:

METHOD A (EASIEST - Use your regular password):
1. Go to https://myaccount.google.com/
2. Click "Security" → "Less secure app access"
3. Turn it ON
4. Use your regular Gmail password

METHOD B (MORE SECURE - Use app password):
1. Go to https://myaccount.google.com/apppasswords
2. Click "Generate" → Select "Mail" → "Windows Computer"
3. Copy the 16-character password Google gives you

STEP 2: Create a .env file in your project folder with:
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_password_or_app_password

Example .env file:
GMAIL_USER=saheli@gmail.com
GMAIL_APP_PASSWORD=your_password_here
'''

def send_email(to_address, subject, body):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print(SETUP_INSTRUCTIONS)
        print(f"\nEmail would be sent to: {to_address}")
        print(f"Subject: {subject}")
        print(f"Body: {body}")
        return False
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent successfully to {to_address}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print("Please check your .env file and Gmail settings.")
        return False

def read_emails(max_emails=5):
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print(SETUP_INSTRUCTIONS)
        return []
    try:
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        mail.select('inbox')
        result, data = mail.search(None, 'ALL')
        mail_ids = data[0].split()
        latest_ids = mail_ids[-max_emails:]
        emails = []
        for i in reversed(latest_ids):
            result, msg_data = mail.fetch(i, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = msg['subject']
            from_ = msg['from']
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
            emails.append({'from': from_, 'subject': subject, 'body': body})
        mail.logout()
        return emails
    except Exception as e:
        print(f"❌ Failed to read emails: {e}")
        print("Please check your .env file and Gmail settings.")
        return []

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
    # Example usage:
    # send_email('recipient@example.com', 'Test Subject', 'Hello from Jarvis!')
    # emails = read_emails()
    # for mail in emails:
    #     print(mail) 