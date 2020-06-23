import smtplib,ssl

def send_email(receiver_email,subject,message):
    port = 465
    sender_email = "thatdoovie@gmail.com"
    receiver_email = "davidawarshawsky@gmail.com"
    password = "Sn2pch2ttingd00vie"

    # Create a secure SSL context
    context = ssl.create_default_context()
    message = """\
Subject: {}
    
{}""".format(subject,message)
    print(message)
    print("From: {}".format(sender_email))
    print("To: {}".format(receiver_email))
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print("sent")

def main():
    send_email("davidawarshawsky@gmail.com","Stock Prediction Stuff","I hope you enjoy")
if __name__ == '__main__':
    main()
