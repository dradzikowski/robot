# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, date

import scrapy
from crawler.db import MongoDBNoCollectionClient
from pymongo import ReturnDocument
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
import re

class GizmodoSpider(CrawlSpider):
    # database connections
    db = MongoDBNoCollectionClient()
    articles_collection = db.client['articles']
    keywords_collection = db.client['keywords']

    # spider settings
    name = "gizmodo"
    allowed_domains = ["gizmodo.com"]
    start_urls = ["http://gizmodo.com"]
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths="//div[contains(@class, 'post-wrapper')]"),
             callback='parse_articles', follow=False),
    )

    # crawled keywords
    crawled_keywords = defaultdict(list)

    # crawling
    def parse_articles(self, response):
        article_contents = response.selector.xpath("//div[contains(@class, 'post-content')]//text()")
        url = str(response.url)
        # what todo with <i> tags? to fix later
        title = response.selector.xpath("//h1[contains(@class, 'headline')]//text()").extract()[0]

        dt = datetime.now()
        date_crawled = str(date(dt.year, dt.month, dt.day))

        if self.is_article_unique(url) and title is not None:
            _id = self.insert_article({"date_crawled": date_crawled,
                                       "title": title,
                                       "url": url,
                                       "site": "gizmodo"
                                       })

            for article_content in article_contents.extract():
                article_content = re.sub(r'\W+', '&', article_content)
                for word in article_content.split('&'):
                    word = word.lower()
                    if str(_id) not in self.crawled_keywords[word]:
                        self.crawled_keywords[word].append(str(_id))

    # indexing
    def closed(self, reason):
        indexing_status = 0;
        indexing_status_percent = 0;
        prev_indexing_status_percent = 0;
        for keyword, references in self.crawled_keywords.iteritems():
            self.keywords_collection.find_one_and_update(
                {"keyword": keyword},
                {"$push": {"references": {'$each': references}}},
                projection={'_id': True},
                upsert=True,
                return_document=ReturnDocument.AFTER
            )

            indexing_status += 1;
            indexing_status_percent = (indexing_status * 100 / len(self.crawled_keywords))
            if indexing_status_percent % 5 == 0 and prev_indexing_status_percent != indexing_status_percent:
                prev_indexing_status_percent = indexing_status_percent
                print 'Indexing: ' + str(indexing_status_percent) + '%'
                print 'Status: ' + str(indexing_status) + ' out of ' + str(len(self.crawled_keywords)) + ' words'

    def is_article_unique(self, url):
        if self.articles_collection.find_one({"url": url}):
            return False
        return True

    def insert_article(self, data):
        return self.articles_collection.insert(data)