from email.mime.text import MIMEText
from datetime import date
import smtplib

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "username@gmail.com"
SMTP_PASSWORD = "password"

EMAIL_TO = SMTP_USERNAME
EMAIL_FROM = SMTP_USERNAME
EMAIL_SUBJECT = "Custom Update : "

DATE_FORMAT = "%d/%m/%Y"


class Email():
	def __init__(self,DATA):
		self.DATA = DATA
		
	def send(self):
		msg = MIMEText(self.DATA)
		msg['Subject'] = EMAIL_SUBJECT + " %s" % (date.today().strftime(DATE_FORMAT))
		msg['To'] = EMAIL_TO
		msg['From'] = EMAIL_FROM
		mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
		mail.ehlo()
		mail.starttls()
		mail.login(SMTP_USERNAME, SMTP_PASSWORD)
		mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
		mail.quit()

if __name__=='__main__':
    Email('testing').send()
