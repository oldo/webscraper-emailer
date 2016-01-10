import smtplib
from recipients_and_app_data import GMAIL_CREDENTIALS

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(recipientAddress):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "AMS Journals"
    msg['From'] = GMAIL_CREDENTIALS['email']
    msg['To'] = recipientAddress

    # Create the body of the message (a plain-text and an HTML version).
    text = "This email needs to be viewed in a client that supports HTML. If you are reading this text then join the 21st century ;-)"
    html = open('scripts/rendered_templates/rendered.html', 'r')

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html.read(), 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(GMAIL_CREDENTIALS['username'], GMAIL_CREDENTIALS['pass'])
    mail.sendmail(GMAIL_CREDENTIALS['email'], recipientAddress, msg.as_string())
    mail.quit()
