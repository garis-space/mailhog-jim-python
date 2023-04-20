import os
import smtplib
from email.mime.text import MIMEText


FROM_EMAIL = "test@example.com"
TO_EMAIL = "test2@example.com"

# Read MailHog's SMTP port from environment variable
SMTP_PORT = os.environ.get('MAILHOG_SMTP_PORT', 1025)


def send_email(from_email, to_email, subject, message):
    # Create email message
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        # Connect to MailHog's SMTP server
        s = smtplib.SMTP('localhost', SMTP_PORT)

        # Send email
        s.sendmail(from_email, to_email, msg.as_string())

        # Uncomment to see the full SMTP conversation
        # s.set_debuglevel(1)

        # Close SMTP connection
        s.quit()

    # Catch ConnectionRefusedError, which is raised when MailHog is not running
    except smtplib.SMTPServerDisconnected as e:
        print(f"ERROR: Connection refused: {e}")

    # Catch SMTPSenderRefused, which is raised when the sender email is invalid
    except smtplib.SMTPSenderRefused as e:
        print(f"ERROR: Sender refused: {e}")

    # Catch SMTPRecipientsRefused, which is raised when the recipient email is invalid
    except smtplib.SMTPRecipientsRefused as e:
        print(f"ERROR: Recipient refused: {e}")

    # Retry send email if it fails
    except Exception as e:
        print(f"ERROR: {e}")
        send_email(from_email, to_email, subject, message)


if __name__ == '__main__':
    # Send email to MailHog SMTP server
    for _ in range(100): # Send 100 emails
        send_email(FROM_EMAIL, TO_EMAIL, 'Test Subject', 'Test Message')
