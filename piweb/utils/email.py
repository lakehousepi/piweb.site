import smtplib

class EmailSender(object):
	def __init__(self, servername, username, password):
		self.servername = servername
		self.username = username
		self.password = password

	def login(self):
		self.server = smtplib.SMTP(self.servername)
		self.server.starttls()
		self.server.login(self.username, self.password)
	
	def logout(self):
		self.server.quit()
		self.server = None
	
	def sendmail(self, fromaddr, toaddrs, subject, body):
		msg = 'Subject: ' + subject + '\n\n' + body
		self.login()
		self.server.sendmail(fromaddr, toaddrs, msg)
		self.logout()