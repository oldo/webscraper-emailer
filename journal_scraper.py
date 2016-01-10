from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def checkForUpdates():
    process = CrawlerProcess(get_project_settings())

    process.crawl('journal')
    process.crawl('article')
    process.start()

if __name__ == '__main__':
    checkForUpdates()
