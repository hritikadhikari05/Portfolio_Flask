import smtplib
from email.mime.text import MIMEText


def send_mail(name, email, message, phone):
    port = 465
    smtp_server = 'smtp.mailtrap.io'
    login = ''
    password = ''
    message = f"<h3>New Contact-info Submission</h3><ul><li>Name: {name}</li><li>Email: {email}</li><li>Message: {message}</li><li>Phone: {phone}</li></ul>"

    sender_email = ''
    receiver_email = ''
    msg = MIMEText(message, 'html')
    msg['Subject'] = f'New Message from  {name}'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
