"""Email OTP verification desktop app.

A Tkinter GUI that emails a 6-digit one-time password (OTP) to the address
entered by the user and then verifies the code they type back.

Configuration is read from environment variables (see .env.example):
    SENDER_EMAIL     - Gmail address used to send the OTP
    SENDER_PASSWORD  - Gmail app password for that account
"""

import os
import re
import secrets
import smtplib
import time
import tkinter as tk
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import font, messagebox, simpledialog, ttk

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
OTP_LENGTH = 6
OTP_TTL_SECONDS = 300  # OTP is valid for 5 minutes
MAX_ATTEMPTS = 3
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class OTPVerificationGUI:
    def __init__(self, sender_email, sender_password):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.otp = ""
        self.otp_created_at = 0.0
        self.setup_gui()

    def setup_gui(self):
        """Build the GUI and start the event loop."""
        self.root = tk.Tk()
        self.root.title("OTP Verification")
        self.root.geometry("500x300")
        self.root.configure(bg="#f3f4f6")

        self.customFont = font.Font(family="Arial", size=12)
        self.headingFont = font.Font(family="Arial", size=16, weight="bold")

        tk.Label(
            self.root, text="OTP Verification System", bg="#f3f4f6", font=self.headingFont
        ).pack(pady=(20, 10))

        tk.Label(
            self.root,
            text="Enter your email and press 'Send OTP'",
            bg="#f3f4f6",
            font=self.customFont,
        ).pack(pady=(0, 20))

        self.email_entry = ttk.Entry(self.root, font=self.customFont)
        self.email_entry.pack(ipadx=5, ipady=5, pady=(0, 20))

        self.send_otp_button = ttk.Button(
            self.root, text="Send OTP", command=self.on_send_otp
        )
        self.send_otp_button.pack(ipadx=5, ipady=5, pady=(0, 10))

        self.root.mainloop()

    def on_send_otp(self):
        """Validate the email, send an OTP, then prompt for it."""
        user_email = self.email_entry.get().strip()
        if not EMAIL_PATTERN.match(user_email):
            messagebox.showerror("Invalid email", "Please enter a valid email address.")
            return

        self.otp = self.generate_otp()
        self.otp_created_at = time.monotonic()
        if self.send_otp_email(user_email, self.otp):
            self.get_user_otp()

    def generate_otp(self):
        """Generate a cryptographically secure numeric OTP."""
        return "".join(str(secrets.randbelow(10)) for _ in range(OTP_LENGTH))

    def send_otp_email(self, user_email, otp):
        """Email the OTP. Returns True on success, False on failure."""
        message = MIMEMultipart()
        message["Subject"] = "Your OTP"
        message["From"] = self.sender_email
        message["To"] = user_email
        minutes = OTP_TTL_SECONDS // 60
        message.attach(
            MIMEText(f"Your OTP is: {otp}\nIt expires in {minutes} minutes.", "plain")
        )

        try:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, user_email, message.as_string())
            messagebox.showinfo("Success", "Email sent successfully")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send email: {e}")
            return False

    def get_user_otp(self):
        """Prompt for the OTP, allowing a limited number of attempts."""
        for attempt in range(1, MAX_ATTEMPTS + 1):
            user_otp = simpledialog.askstring(
                "OTP", f"Enter the OTP sent to your email (attempt {attempt}/{MAX_ATTEMPTS}):"
            )
            if user_otp is None:  # dialog cancelled
                return
            if self.verify_otp(user_otp.strip(), self.otp):
                return
        messagebox.showerror("Failed", "Too many failed attempts. Please request a new OTP.")
        self.otp = ""

    def verify_otp(self, user_otp, real_otp):
        """Check the OTP against the generated one. Returns True if valid."""
        if time.monotonic() - self.otp_created_at > OTP_TTL_SECONDS:
            messagebox.showerror("Expired", "OTP has expired. Please request a new one.")
            return False
        if real_otp and secrets.compare_digest(user_otp, real_otp):
            messagebox.showinfo("Verified", "OTP Verified. Access Granted.")
            return True
        messagebox.showerror("Failed", "Invalid OTP. Access Denied.")
        return False


def main():
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")
    if not sender_email or not sender_password:
        raise SystemExit(
            "Missing SENDER_EMAIL / SENDER_PASSWORD environment variables. "
            "See .env.example and README.md."
        )
    OTPVerificationGUI(sender_email, sender_password)


if __name__ == "__main__":
    main()
