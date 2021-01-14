import smtplib

user_name = 'gs454236@gmail.com'
user_pass = 'bbbshyaw'

def init_smtp(sender, receiver, message):
    try:
        server  = smtp.SMTP_SSL('smtp.gmail.com', 587)
        server.ehlo()   # optional handshake
        server.login(user_name, user_pass)

        print('.....Successfully connected to smtp.gmail.com.......')


        server.close()
    except Error as e:
        print(e)
        print('[-] Error: Unable to secure connection')

def send(sender, receiver, message):
    try:
        server  = smtp.SMTP_SSL('smtp.gmail.com', 587)
        server.ehlo()   # optional handshake
        server.login(user_name, user_pass)

        server.sendmail(sender, receiver, message)

        server.close()
    except Error as e:
        print(e)
        print('[-] Error: Unable to send email')



