import smtplib
import email.mime.text
import email.utils


def create_mimetext(address, subject, body):
    message = email.mime.text.MIMEText(body)
    message['Subject'] = subject
    message['From'] = address['from']
    message['To'] = address['tos']
    message['Bcc'] = address.get('bccs')
    message['Date'] = email.utils.formatdate()
    return message


def _mail_send(smtp_host, smtp_port, addrs, password, mimetext):
    smtpobj = smtplib.SMTP(smtp_host, smtp_port)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(addrs['from'], password)
    smtpobj.sendmail(addrs['from'], addrs['tos'], mimetext.as_string())
    smtpobj.close()


def gmail_send(addrs, password, subject, body):
    _mail_send('smtp.gmail.com', 587,
               addrs, password, create_mimetext(addrs, subject, body))
