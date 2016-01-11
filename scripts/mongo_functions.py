from pymongo import MongoClient

client = MongoClient()
db = client['AMS-Journals']  # database name

articlesCollection = db['articles']  # db collection
journalsCollection = db['journals']  # db collection


def checkForNewArticles():
    testArticle = articlesCollection.count({"emailed": False})
    if testArticle:
        print("\n**************************************\n")
        print(str(testArticle) + " new article(s) found")
        return True
    else:
        print("\n**************************************")
        print("\nNo new articles found")
        print("\n**************************************")
        return False


def markEmailedArticles():
    print("Marking sent articles as emailed")
    print("\n**************************************")
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


if __name__ == "__main__":
    getUnemailedArticles()
