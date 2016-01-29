# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, date
from crawler.db import MongoDBClient
from crawler.db import MongoDBNoCollectionClient
from pymongo import ReturnDocument
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import re


# TODO DIFFER COLLECTIONS
class TechCrunchSpider(CrawlSpider):
    # database connections
    db = MongoDBNoCollectionClient()
    articles_collection = db.client['articles']
    keywords_collection = db.client['keywords']

    # spider settings
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["http://techcrunch.com/"]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths="//a[contains(@class, 'read-more')]"), callback='parse_articles',
             follow=True),
    )

    # crawled keywords
    crawled_keywords = defaultdict(list)

    # crawling
    def parse_articles(self, response):
        # TODO: caching titles not to check in db each time
        #art_date = response.selector.xpath("//div[contains(@class, 'title-left')]//time/@datetime")
        title = response.selector.xpath("//header[contains(@class, 'article-header')]//h1/text()")
        article_contents = response.selector.xpath("//div[contains(@class, 'article-entry')]//text()")
        articles = response.selector.xpath("//div[contains(@class, 'article-entry')]//text()")
        article = articles[0]

        dt = datetime.now()
        date_crawled = str(date(dt.year, dt.month, dt.day))

        # keywords
        extract = article.extract().split()

        # url
        url = str(response.url)

        # title
        title = title.extract()[0]

        if self.isArticleUnique(url):

            _id = self.insert_article({"date_crawled": date_crawled,
                           "title": title,
                           "url": url,
                           "site": "techcrunch"
                           # for other crawlers
                           # datetime.datetime.strptime('2015-12-31', "%Y-%m-%d").date().isoformat()
                           # "art_date": art_date.extract()[0]
                           })

            for article_content in article_contents.extract():
                article_content = re.sub(r'\W+', '&', article_content)
                for word in article_content.split('&'):
                    word = word.lower()
                    if str(_id) not in self.crawled_keywords[word]:
                        self.crawled_keywords[word].append(str(_id))

    def closed(self, reason):
        for keyword, references in self.crawled_keywords.iteritems():  # self.crawledKeywords:
            self.keywords_collection.find_one_and_update(
                {"keyword": keyword},
                {"$push": {"references": {'$each': references}}},
                projection={'_id': True},
                upsert=True,
                return_document=ReturnDocument.AFTER
            )

    def insert_article(self, data):
        return self.articles_collection.insert(data)

    def isArticleUnique(self, url):
        if self.articles_collection.find_one({"url": url}):  # TODO limit to last 10 arts?
            return False
        return True
