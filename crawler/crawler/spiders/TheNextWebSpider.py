# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, date
from crawler.db import MongoDBNoCollectionClient
from pymongo import ReturnDocument
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class TheNextWebSpider(CrawlSpider):
    # database connections
    db = MongoDBNoCollectionClient()
    articles_collection = db.client['articles']
    keywords_collection = db.client['keywords']

    # spider settings
    name = "thenextweb"
    allowed_domains = ["thenextweb.com"]
    start_urls = ["http://thenextweb.com/"]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths="//li[contains(@class, 'postCard--story')]"),
             callback='parse_articles', follow=False),
    )

    # crawled keywords
    crawled_keywords = defaultdict(list)

    # crawling
    def parse_articles(self, response):
        article_contents = response.selector.xpath("//div[contains(@class, 'postContent')]//text()")
        url = str(response.url)
        title = response.selector.xpath("//h1[contains(@class, 'title')]//text()").extract()[0]
        #if title is
        dt = datetime.now()
        date_crawled = str(date(dt.year, dt.month, dt.day))

        if self.is_article_unique(url) and title is not None:
            _id = self.insert_article({"date_crawled": date_crawled,
                                       "title": title,
                                       "url": url,
                                       "site": "thenextweb"
                                       })

            for article_content in article_contents.extract():
                for word in article_content.split():
                    if str(_id) not in self.crawled_keywords[word]:
                        self.crawled_keywords[word].append(str(_id))

    # indexing
    def closed(self, reason):
        for keyword, references in self.crawled_keywords.iteritems():
            # trim commas and dots
            self.keywords_collection.find_one_and_update(
                {"keyword": keyword},
                {"$push": {"references": {'$each': references}}},
                projection={'_id': True},
                upsert=True,
                return_document=ReturnDocument.AFTER
            )

    def is_article_unique(self, url):
        if self.articles_collection.find_one({"url": url}):
            return False
        return True

    def insert_article(self, data):
        return self.articles_collection.insert(data)
