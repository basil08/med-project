
"""
This program is part of the Arghya Birthday Surprise Cryptographic Puzzle (ABSCP)
To read more about it, goto: 

It sends a custom email(in the body variable) called 'The Invitation'(After cicada 3301)  to 'royarghya13@gmail.com'
from 'gs454236@gmail.com'..which is Purple Santa(my auxiliary gmail account)

@author: Basil Labib ...mostly copied from geeksforgeeks
@date: 12apr2020
"""

# Python code to illustrate Sending mail with attachments 
# from your Gmail account  

# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
   
fromaddr = "gs454236@gmail.com"
# toaddr = "royarghya13@gmail.com"
toaddr = "basillabib01@gmail.com"   

# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# storing the senders email address   
msg['From'] = fromaddr 
  
# storing the receivers email address  
msg['To'] = toaddr 
  
# storing the subject  
msg['Subject'] = "THE PURPLE SANTA HAS YOU! Are you ready for it?"
  
# string to store the body of the mail 
body = "Hello.\nThis is not a spam or a hoax. Hoaxes and spams don't have puzzles.\
\n\nIf you wish to quit, send a mail to this id with the text 'I quit'.\nOr if you give up on a certain arena, send 'Help' and your whereabouts.\n\n\
We hope you are ready to venture on your path. All the best.\n\nKeep these. You will need them later. And remember Vernam might help you then.\n119 107 107 111 108 37 48 48 118 114 120 106 109 49 124 112 114 48 126 48 69 107 81 79 105 43 79\n\n\
Abandon all hopes and enter the hall.\nWith the prime despised by all.\nlxxtw>33mqkyv2gsq3e3HEXrx;y\n\nPS:Think simple.\n\n\
Good luck.\nPurple Santa."
  

# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
# filename = "File_name_with_extension"
# attachment = open("Path of the file", "rb") 
  
# instance of MIMEBase and named as p 
# p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
# p.set_payload((attachment).read()) 
  
# encode into base64 
# encoders.encode_base64(p) 
   
# p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
# msg.attach(p) 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login(fromaddr, "summerhead_2006") 
  
# Converts the Multipart msg into a string 
text = msg.as_string() 
  
# sending the mail 
s.sendmail(fromaddr, toaddr, text) 
  
# terminating the session 
s.quit() 
