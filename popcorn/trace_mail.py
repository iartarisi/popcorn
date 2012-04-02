from popcorn.configs import SMTP_PORT,SMTP_SERVER,HOST_EMAIL,HOST_PASS,ADMIN_MAIL,MESSAGE
import sys
import traceback
from smtplib import SMTPException
import smtplib

def mail_to_admin(traceback):
	try:
		smtpObj=smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.login(HOST_EMAIL,HOST_PASS)
		message=MESSAGE+str(traceback)
		smtpObj.sendmail(HOST_EMAIL,ADMIN_MAIL,message)
	except SMTPException:
		print 'Error while sending email'
		
	
	
	
	
