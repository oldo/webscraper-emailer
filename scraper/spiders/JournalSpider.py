from scrapy import Spider
import re
from lxml.html.clean import Cleaner  # remove HTML tags

from scraper.items import JournalItem


# helper function to remove newline characters: \n \t \r
def removeNewlines(stringIn):
    stringOut = re.sub('\s+', ' ', stringIn)
    return stringOut


class JournalSpider(Spider):
    name = "journal"
    allowed_domains = ["ametsoc.org"]

    journalURLIdentifiers = [
        "bams",
        "eint",
        "apme",
        "atot",
        "clim",
        "hydr",
        "phoc",
        "atsc",
        "mwre",
        "wefo",
        "wcas"
    ]

    # create list of all urls to be scraped
    start_urls = []
    for url in journalURLIdentifiers:
        start_urls.append("http://journals.ametsoc.org/toc/" + url + "/current")

    def parse(self, response):
        item = JournalItem()

        base_url = "http://journals.ametsoc.org"

        journalTitle = response.xpath('//*[@id="journalBlurbPanel"]/div[2]/h3/text()').extract_first()
        item['title'] = journalTitle

        journalIssue = response.xpath('//*[@id="articleToolsHeading"]/text()').extract_first().strip()  # remove whitespace at start and end
        item['issue'] = journalIssue

        # setup html cleaner to strip html tags from string (journal titles often use sub/superscript and splits article title)
        html_cleaner = Cleaner(allow_tags=[''], remove_unknown_tags=False)

        journalDescription = response.xpath('//*[@id="journalBlurbPanel"]/div[4]').extract()
        journalDescription = "".join(journalDescription)
        journalDescription = html_cleaner.clean_html(journalDescription)[5:-6]  # remove any html tags and then trim the <div> tags that the cleaner inserts
        journalDescription = removeNewlines(journalDescription)  # remove any \n\r\t characters
        journalDescription = journalDescription.strip()
        item['description'] = journalDescription

        coverImage = response.xpath('//*[@id="smallIssueCover"]/img/@src').extract_first().strip()
        print(coverImage)
        item['coverURL'] = base_url + coverImage

        yield item
