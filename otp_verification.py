import smtplib
import ssl
import secrets
from email.mime.text import MIMEText
import re

# Function to send OTP email
def send_otp_email(receiver_email, otp):
    sender_email = "samyuktapathak1131@gmail.com"  # Sender email address
    password = "mauvtjaqluphqrzl"  # Sender email password
    subject = "OTP for Verification"
    message = f"Your OTP for Login Verification is: {otp}"

    msg = MIMEText(message)
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Function to generate OTP
def generate_otp():
    return str(secrets.randbelow(1000000)).zfill(6)

# Function to verify OTP
def verify_otp(input_otp, generated_otp):
    return input_otp == generated_otp

# Function to validate email format
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)
