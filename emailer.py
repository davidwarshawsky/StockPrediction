from email.headerregistry import Address
from email.message import EmailMessage
import os
import smtplib



def create_email(subject, body):
    email_address = 'thatdoovie@gmail.com'
    # Recipient
    to_address = (
        Address(display_name='David Warshawsky', username='davidawarshawsky', domain='gmail.com'),
    )
    msg = EmailMessage()
    msg['From'] = email_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body)
    print(msg)
    return msg

def send_email(email):
    email_address = 'thatdoovie@gmail.com'
    email_password = 'Sn2pch2ttingd00vie'
    with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(email_address, email_password)
        smtp_server.send_message(email)

def main():
    email = create_email("AppliedMarkets Welcomes You","We hope you are doing well!")
    send_email(email)

if __name__ == '__main__':
    main()