from email.headerregistry import Address
from email.message import EmailMessage
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import sys


def create_text_email(subject, body):
    email_address = 'thatdoovie@gmail.com'
    # Recipient
    to_address = (
        Address(display_name='AppliedMarkets', username='davidawarshawsky', domain='gmail.com'),
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
    email_password = 'mmhbfZAu2UPOFoksty1nGtfVjZYaVokwvPMd6dcE7ksFI5AYI5Vw'
    with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(email_address, email_password)
        smtp_server.send_message(email)

def create_html_email_from_df(name,email,df1,df2):
    msg = MIMEMultipart()
    msg['Subject'] = "AppliedMarkets Predictions"
    msg['From'] = "AppliedMarkets"
    msg['To'] = email
    # https://stackoverflow.com/questions/46620604/python-mime-attaching-multiple-attachments-to-a-multipart-message
    # The above link explains that the reason you can't send MimeMultipart with multiple text and html is because the last
    # part to be attached is the one considered that you want to add. If the HTML fails then at least the text is shown.
    # This does not mean that you can put text1,html2,text3,html4 into the email.
    # https://stackoverflow.com/questions/50564407/pandas-send-email-containing-dataframe-as-a-visual-table
    title = 'Biggest Predicted Adjusted Close Stock Price 10 Days From 08/04/2020'
    intro = """
    Hi {0},<br>
    Our predictions use state of the art Artificial Intelligence(AI) models to attempt to predict the stock market.
     The predictions below are split into two sections:<br>"""\
        .format(name)
    ordered_list = """
    <ol>
        <li>The predicted increase percent change of the adjusted close of stocks 10 market days from the end of trading
        day Tuesday 08-04-2020<br>. They are ordered from top to bottom by largest percent increase in adjusted close.</li>
    
        <li>The predicted decrease percent change of the adjusted close of stocks 10 market days from the end of trading
        day Tuesday 08-04-2020<br>. They are ordered from top to bottom by largest percent decrease in adjusted close.</li>
    </ol>
    """
    section_one = "Section 1):"
    section_two = "Section 2):<br>"

    end = """<br>
    We would appreciate any feedback on our Website http://localhost<br>
    Best Regards, <br>
    David Warshawsky and Elad Warshawsky<br><br>
    Disclaimer: This is purely for entertainment and does not constitute financial advice.
    """
    text = intro + df1.to_string() + section_two + df2.to_string() + end
    general = """\
        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="UTF-8">
            <style>
                table {float: left; font-size: 20px;font-weight:bold}
                p {font-size: 18px;}
                ol {font-size: 22px;}
                .float-container {padding: 20px; width: 100%%;}
                .float-child1 {float: left;}
                .float-child2 {float: left; margin-left: 100px;}
            </style>
            <!-- Title -->
            <title>%s</title>
          </head>
          <body>
            <div>
                <!-- Intro  -->
                <p>%s</p>
                %s
                <!-- Two tables side by side -->
                <div class = "float-container">
                    <div class = "float-child1">
                        <h1>%s</h1>
                        %s
                    </div>
                    <div class = "float-child2">
                        <h1>%s</h1>
                        %s
                    </div>
                </div>
                <div>
                    <!-- Ending statement -->
                    <p><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>%s</p>
                </div>
            </div>
          </body>
        </html>
        """
    html = general % (title,intro,ordered_list,section_one,df1.to_html(),section_two,df2.to_html(),end)
    print(os.getcwd())
    pred_email_path = '..{0}infrastructure{0}pred_email.html'.format(os.path.sep)
    with open(pred_email_path,'w') as pred_email:
        pred_email.write(html)


    # part1 = MIMEText(text,"plain")
    part2 = MIMEText(html, 'html')

    # msg.attach(part1)
    msg.attach(part2)
    return msg


def prediction_df_transformer():
    # print(os.getcwd())
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    pred_path = 'C:{0}Projects{0}StockPrediction{0}data{0}stock_data{0}predictions{0}08-04-2020predictions.html'.format(os.path.sep)
    with open(pred_path, 'r') as f:
        contents = f.read()
        soup = bs(contents, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    df = df.iloc[:,2:]
    # Drop index because it gives Unnamed in the table.
    df.reset_index(drop=True)
    # Drop all columns with all missing values
    df.dropna(how='all',axis='columns')
    # Get the predictions for ten days ahead.
    new_df = pd.DataFrame(df.iloc[-1, :],index=df.columns)
    new_df.dropna()
    #  Looked up error and food this website https://www.barchart.com/stocks/performance/gap/gap-up
    new_df = new_df.sort_values(by=new_df.columns[0], axis=0)
    new_df.columns = ['Percent change(%) increase or decrease in adjusted close for stocks 10 trading days from Tuesday 08/04/2020'.replace(" ","_")]
    # print(new_df.shape)
    # print(new_df.head(20))
    return new_df

def get_positive(df):
    positive_df = df[(df[df.columns] > 0).all(axis=1)]
    positive_df.sort_values(by=positive_df.columns[0], ascending=False,inplace=True,axis=0)
    positive_df.columns = ['Positive % change increases']
    return positive_df

def get_negative(df):
    negative_df = df = df[(df[df.columns] < 0).all(axis=1)]
    negative_df.sort_values(by=negative_df.columns[0],ascending=True,inplace=True,axis=0)
    negative_df.columns = ['Negative % change increases']
    return negative_df

def get_zero(df):
    zero_df = df = df[(df[df.columns] == 0).all(axis=1)]
    zero_df.sort_values(by=zero_df.columns,ascending=False,inplace=True)
    zero_df.columns = ['Zero % change increases']
    return zero_df



def main():
    preds = prediction_df_transformer()
    pos_preds = get_positive(preds).head(10)
    neg_preds = get_negative(preds).head(10)
    # email = create_html_email_from_df('Ron',"ron@memfix.com",pos_preds,neg_preds)
    # email = create_html_email_from_df('Elad', "eladwarshawsky@gmail.com", pos_preds, neg_preds)
    email = create_html_email_from_df('David','davidawarshawsky@gmail.com',pos_preds,neg_preds)
    # send_email(email)

if __name__ == '__main__':
    main()