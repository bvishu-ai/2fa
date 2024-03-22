import tkinter as tk
from tkinter import messagebox
import pyotp
import smtplib
import ssl
import secrets
from email.mime.text import MIMEText
import re

# Simulated user database
users = {
    "samyukta": {
        "password": "password123",
        "secret_key": "JBSWY3DPEHPK3PXP"
    },
    "vishal": {
        "password": "securepass",
        "secret_key": "MFRGGZDFMZTWQ2LK"
    }
}

# Create a GUI window
window = tk.Tk()
window.title("2FA Login")

# Function to send otp in email using smtp protocol
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

def check_otp(totp, otp_entry):
    if totp.now() == otp_entry:
        messagebox.showinfo("Success", "Successful Login")
    else:
        messagebox.showerror("Error", "Invalid OTP")

# Function to perform authentication
def authenticate():
    # Get the entered username and password
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    # Check if the username exists in the user database
    if username in users:
        stored_password = users[username]["password"]
        secret_key = users[username]["secret_key"]

        # Verify the entered password against the stored password
        if password == stored_password:
            # Generate the OTP based on the secret key
            totp = pyotp.TOTP(secret_key)
            otp = totp.now()
            
            # Display the OTP in a message box
            messagebox.showinfo("OTP", f"The OTP has been sent to the email {email}")
            send_otp_email(email, otp)
            window.destroy()
            window2 = tk.Tk()
            window2.title("OTP Entry")
            otp_label = tk.Label(window2, text="Enter the OTP:")
            otp_label.pack()
            otp_entry = tk.Entry(window2)
            otp_entry.pack()

            login_button = tk.Button(window2, text="Login", command = lambda: check_otp(totp, otp_entry.get()))
            login_button.pack(pady=10)

            window2.mainloop()
        else:
            messagebox.showerror("Error", "Invalid password")
    else:
        messagebox.showerror("Error", "Invalid username")

# Create username label and entry field
username_label = tk.Label(window, text="Username:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

# Create password label and entry field
password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

# Create a email label and entry field
email_label = tk.Label(window, text="Enter E-Mail for OTP Generation:")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

# Create a login button
genotp_button = tk.Button(window, text="Generate OTP", command=authenticate)
genotp_button.pack(pady=10)

# Run the GUI main loop
window.mainloop()
