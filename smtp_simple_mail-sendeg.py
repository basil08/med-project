#Python code to illustrate Sending mail from  
# your Gmail account  
import smtplib 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 


sender = 'gs454236@gmail.com'
receiver = 'royarghya13@gmail.com'
password = '2a19i12_12a2i2'
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login(sender, password) 
  
# message to be sent 

message = "Hello Purple Santa from Python!"  
# sending the mail 


s.sendmail(sender, receiver, message)
  
# terminating the session 
s.quit() 