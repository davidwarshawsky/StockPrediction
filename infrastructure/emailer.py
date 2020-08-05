from email.headerregistry import Address
from email.message import EmailMessage
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import sys


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

def create_html_email_from_df(to,df):
    # https: // docs.python.org / 3.7 / library / email.examples.html
    msg = MIMEMultipart()
    msg['Subject'] = "AppliedMarkets predictions for today"
    msg['From'] = Address("David Warshawsky", "davidawarshawsky", "gmail.com")
    msg['To'] = (Address("Elad Warshawsky", "eladwarshawsky", "gmail.com"),
                 Address("Ron Warshawsky", "ron", "memfix.com"))
    # https://stackoverflow.com/questions/50564407/pandas-send-email-containing-dataframe-as-a-visual-table
    html = """\
    <html>
      <head></head>
      <body>
        {0}
      </body>
    </html>
    """.format(df.to_html())

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.sendmail(msg['From'], emaillist, msg.as_string())
def main():
    email = create_email("AppliedMarkets Welcomes You","We hope you are doing well!")
    send_email(email)

if __name__ == '__main__':
    main()
