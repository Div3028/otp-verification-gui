# Email OTP Verification

A Python desktop app (Tkinter) that verifies a user's email address with a one-time password. It emails a 6-digit code through Gmail SMTP, then checks the code the user types back.

## Features
- Simple Tkinter GUI
- Cryptographically secure OTP (`secrets`)
- Code expires after 5 minutes, maximum 3 attempts
- Email format validation
- Credentials loaded from environment variables, never hard-coded
- No third-party dependencies

## Quick start (short version)
```powershell
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
$env:SENDER_EMAIL = "your_email@gmail.com"
$env:SENDER_PASSWORD = "your_gmail_app_password"
python otp_verification.py
```

## Full setup, step by step

### 1. Install Python
- Download Python 3.8+ from https://www.python.org/downloads/.
- On Windows, tick **Add Python to PATH** and keep **tcl/tk** selected in the installer.
- Check it works: `python --version`

### 2. Get the project
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```
Or download the ZIP from GitHub and extract it.

### 3. Create a Gmail App Password
The app sends the email from a Gmail account you own. Gmail needs an app password, not your normal password.
1. Open https://myaccount.google.com/security and turn on **2-Step Verification**.
2. Open https://myaccount.google.com/apppasswords.
3. Create an app password (name it e.g. "OTP App"). Copy the 16-character code.

### 4. Set your credentials
Use your own values. These are stored only in your terminal session, not in any file in the repo.

**Windows (PowerShell):**
```powershell
$env:SENDER_EMAIL = "your_email@gmail.com"
$env:SENDER_PASSWORD = "your_gmail_app_password"
```

**macOS / Linux:**
```bash
export SENDER_EMAIL="your_email@gmail.com"
export SENDER_PASSWORD="your_gmail_app_password"
```

Alternative: copy `.env.example` to `.env` and fill it in. `.env` is git-ignored. The app does not read `.env` itself, so set the variables as shown above (or load the file with your shell or IDE).

### 5. Run
```bash
python otp_verification.py
```

### 6. Use it
1. Enter the recipient email and click **Send OTP**.
2. Check that inbox (and spam) for the code.
3. Type the code in the dialog. You get 3 attempts within 5 minutes.

## Troubleshooting
| Problem | Fix |
|---|---|
| `Missing SENDER_EMAIL / SENDER_PASSWORD` | Set the variables in the same terminal you run the app from. |
| `Username and Password not accepted` | Use an App Password (step 3), not your normal password. |
| `No module named tkinter` | Reinstall Python with tcl/tk, or on Linux `sudo apt install python3-tk`. |
| Email not arriving | Check spam; confirm the address is correct. |

## Security notes
- Never commit real credentials. `.env` and local-only files are listed in `.gitignore`.
- If a password is ever exposed, revoke it at https://myaccount.google.com/apppasswords.
- This is an educational demo. A production system should store OTPs server-side, rate-limit requests per user and use a transactional email service.

## License
MIT. See [LICENSE](LICENSE).
