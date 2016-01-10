from pymongo import MongoClient

client = MongoClient()
db = client['AMS-Journals']

articlesCollection = db['articles']
journalsCollection = db['journals']


def checkForNewArticles():
    if articlesCollection.find({"emailed": False}):
        return True
    else:
        return False


def markEmailedArticles(articles):
    for article in articlesCollection.find({'emailed': False}):
        article['emailed'] = True
        articlesCollection.update({'title': article['title']}, article, upsert=True)


def getTemplateContext():
    context = []

    # create a list of journals with new articles to iterate over and query mongodb
    journals = []
    for journal in articlesCollection.find({"emailed": False}).distinct("journalTitle"):
        journals.append(journal)

    # create a list of dictionaries each containing info and new articles for a single journal
    # dictionaries of the form:
    # "title": journal title
    # "issue":
    # "coverURL":
    # "description": blurb about the journal
    # "articles": [a list of all new articles]

    for journal in journals:
        # find the journal details (title, issue, converURL)
        dict = {}
        dict = journalsCollection.find_one({"title": journal})

        # find all the new articles for the journal
        articles = []
        for article in articlesCollection.find({"journalTitle": journal, "emailed": False}):
            articles.append(article)
        dict["articles"] = articles

        context.append(dict)

    contextDict = {"context": context}
    return contextDict


def getUnemailedArticles():
    articles = []

    for article in articlesCollection.find({'emailed': False}):
        articles.append(article)

    if not articles:
        print("There were no new articles to retrieve")
    return articles


if __name__ == "__main__":
    getUnemailedArticles()
