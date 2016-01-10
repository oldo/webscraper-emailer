# AMS Journal website scraping and emailing script

from recipients_and_app_data import recipients
from journal_scraper import checkForUpdates
from scripts.mongo_functions import checkForNewArticles, markEmailedArticles
from scripts.render_template import renderTemplate
from scripts.emailer import sendEmail


def main():
    checkForUpdates()  # Check for new articles and pull to db if they exist:

    if checkForNewArticles():
        # loop through the recipients and render/send an email to each of them
        for recipient in recipients:
            renderTemplate(recipient['name'])
            sendEmail(recipient['email'])

        # mark sent emails in db
        markEmailedArticles()


if __name__ == '__main__':
    main()
