import email.mime.multipart as mp
import email.mime.text as tx
import smtplib

from utils.config import gdocs

class EmailSender(object):
    def __init__(self, servername=None, username=None, password=None):
        self.servername = servername if servername is not None else gdocs.SERVERNAME
        self.username = username if username is not None else gdocs.USERNAME
        self.password = password if password is not None else gdocs.PASSWORD

    def login(self):
        self.server = smtplib.SMTP(self.servername)
        self.server.starttls()
        self.server.login(self.username, self.password)

    def logout(self):
        self.server.quit()
        self.server = None

    def sendmail(self, fromaddr, toaddrs, subject, body):
        msg = 'From: ' + fromaddr + '\n'
        msg += 'To: ' + ', '.join(toaddrs) + '\n'
        msg += 'Subject: ' + subject + '\n\n'
        msg += body
        self.login()
        self.server.sendmail(fromaddr, toaddrs, msg)
        self.logout()

    def sendmail_html(self, fromaddr, toaddrs, subject, textbody, htmlbody):
        msg = mp.MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = ', '.join(toaddrs)

        if textbody is not None:
            part1 = tx.MIMEText(textbody, 'plain')
            msg.attach(part1)
        if htmlbody is not None:
            part2 = tx.MIMEText(htmlbody, 'html')
            msg.attach(part2)

        self.login()
        self.server.sendmail(fromaddr, toaddrs, msg.as_string())
        self.logout()
