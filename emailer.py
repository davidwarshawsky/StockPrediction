import smtplib,ssl

port = 465
password = "Sn2pch2ttingd00vie"

# Create a secure SSL context
context = ssl.create_default_context()

sender_email = "thatdoovie@gmail.com"
receiver_email = "davidawarshawsky@gmail.com"
message = """\
Subject: StockShock predictions!

Hello David, I am David from StockShock, here are your predictions!
"""

with smtplib.SMTP_SSL("thatdoovie@gmail.com", port, context=context) as server:
    server.login("thatdoovie@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)