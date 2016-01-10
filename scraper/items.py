from scrapy.item import Item, Field


class ArticleItem(Item):
    journalTitle = Field()
    journalIssue = Field()
    title = Field()
    url = Field()
    emailed = Field()


class JournalItem(Item):
    title = Field()
    issue = Field()
    coverURL = Field()
    description = Field()
