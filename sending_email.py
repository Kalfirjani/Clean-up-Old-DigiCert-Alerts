import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def send_email(email_body):
    sender_email = ""
    receiver_email = ""
    password = ""

    #Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "multipart test"
    msg["From"] = ''
    msg["To"] = ''
    msg.set_content = email_body
    msg.attach(MIMEText(email_body, 'html'))
    # Create secure SMTP connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, msg.as_string()
        )
