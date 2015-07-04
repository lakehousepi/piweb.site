import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
        msg = 'From: ' + fromaddr + '\n'
        msg += 'To: ' + ', '.join(toaddrs) + '\n'
        msg += 'Subject: ' + subject + '\n\n'
        msg += body
        self.login()
        self.server.sendmail(fromaddr, toaddrs, msg)
        self.logout()

    def sendmail_html(self, fromaddr, toaddrs, subject, textbody=None, htmlbody=None):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = fromaddr
        msg['To'] = ', '.join(toaddrs)

        if textbody is None:
            textbody = 'Hello World'
        if htmlbody is None:
            htmlbody = """\
                        <html>
                          <head></head>
                          <body>
                            <p>Hi!<br>
                               How are you?<br>
                               Here is the <a href="http://www.python.org">link</a> you wanted.
                            </p>
                          </body>
                        </html>
                        """

        part1 = MIMEText(textbody, 'plain')
        part2 = MIMEText(htmlbody, 'html')

        msg.attach(part1)
        msg.attach(part2)
        self.login()
        self.server.sendmail(fromaddr, toaddrs, msg.as_string())
        self.logout()
