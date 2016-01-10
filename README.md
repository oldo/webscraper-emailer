# American Journal of Meteorology New Article Notifier

The following setup will scrape all of the *current issue* pages for AJM's various journals to search for new articles. If new articles are found then a summary email is created and sent to anyone who is on the recipients list.

With some modification I'm sure it could be adapted to scrape any other page and automatically email a list of recipients.

# How It Works

All programmed in Python

Scrapy > MongoDB > Jinja2 > Email delivery with SMTPLib via gmail

# Installation

* MongoDB must be installed and `mongod` running.
* `$ pip install -r requirements.txt`
* The script depends on a file that I've excluded from git which has the gmail login details and a list of the recipients. It is located in the root directory of the project and is of the form:
  ```python
  recipients = [
      {
          'name': 'Oliver',
          'email': 'oldo.nicho AT gmail.com'
      },
      {
          'name': 'Nollie',
          'email': 'oldo.nicho1 ATgmail.com'
      }
  ]

  GMAIL_CREDENTIALS = {
      'email': 'senders email address',
      'username': 'gmail username',
      'pass': 'gmail password'
  }
  ```
* Run `$ python main.py`
* Setup a cron job to run the script at any interval that you desire.
