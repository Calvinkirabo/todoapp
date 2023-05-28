import time
import smtplib

 
subject = 'Reminder: Your task is due tomorrow'
body = 'Dear user,\n\nThis is a friendly reminder that your task is due tomorrow. Please complete it by the deadline.\n\nBest regards,\nYour Reminder App'
message = f'Subject: {subject}\n\n{body}'

 
delay_seconds = 360

 
time.sleep(delay_seconds)

 
sender_email = 'your-email@gmail.com'
sender_password = 'your-email-password'
to_email = 'recipient-email@gmail.com'

 
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, sender_password)
    smtp.sendmail(sender_email, to_email, message)
