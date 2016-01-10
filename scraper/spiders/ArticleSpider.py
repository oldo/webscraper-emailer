from scrapy import Spider
from lxml.html.clean import Cleaner  # remove HTML tags

from scraper.items import ArticleItem


class ArticleSpider(Spider):
    name = "article"
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
        base_url = "http://journals.ametsoc.org"

        journalTitle = response.xpath('//*[@id="journalBlurbPanel"]/div[2]/h3/text()').extract_first()
        journalIssue = response.xpath('//*[@id="articleToolsHeading"]/text()').extract_first().strip()  # remove whitespace at start and end

        # setup html cleaner to strip html tags from string (journal titles often use sub/superscript and splits article title)
        html_cleaner = Cleaner(allow_tags=[''], remove_unknown_tags=False)

        # find all articles for the issue and parse each one individually
        articles = response.xpath('//div[@id="rightColumn"]//table[@class="articleEntry"]')

        for article in articles:
            item = ArticleItem()
            item['journalTitle'] = journalTitle
            item['journalIssue'] = journalIssue
            # the article title is not always a single string and can be divided up to have HTML formatting (sub/superscript, italics, etc.)
            # therefore the entire article title including all HTML has to be scraped then tags removed.
            title = article.xpath('.//div[@class="art_title"]').extract()
            title = "".join(title)  # joins the list object to one string
            item['title'] = html_cleaner.clean_html(title)[5:-6]  # remove html tags from title and then trim the <div> tags that the cleaner inserts
            item['url'] = base_url + article.xpath('.//a/@href').extract_first()
            item['emailed'] = False  # boolean to indicate whether article has been emailed to list
            yield item
