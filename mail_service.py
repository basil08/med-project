import os

"""
Email Service: send simple plain-text emails via SMTP.
FROM_ADDR, FROM_ADDR_PASS are set already.

TODO: When env is used, ensure FRom_ADDR and FROM_ADDR_PASS are defined

"""
# MAIL_PASS = os.environ.get('MAIL_PASS', None)
# MAIL_ID = os.environ.get('MAIL_ID', None)

MAIL_PASS = os.getenv('MAIL_PASS')
MAIL_ID = os.getenv('MAIL_ID')

# Python code to illustrate Sending mail with attachments 
# from your Gmail account  

# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def send(toaddr, subject, body):
    """
    Send an email with subject and body to toaddr. 
    TODO: Sender id can be configured from admin panel
    """
        
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    
    # storing the senders email address   
    msg['From'] = MAIL_ID
    # storing the receivers email address  
    msg['To'] = toaddr 
    
    # storing the subject  
    msg['Subject'] = subject
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
    
    # creates SMTP session 
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587) 
        # start TLS for security 
        s.starttls() 
        # Authentication 
        s.login(MAIL_ID, MAIL_PASS)
        # Converts the Multipart msg into a string 
        text = msg.as_string() 
        # sending the mail 
        s.sendmail(MAIL_ID, toaddr, text) 
    except:
        print("Error: Could not send message to {}".format(toaddr))
    finally:
        s.quit()