# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, date
from crawler.db import MongoDBClient
from pymongo import ReturnDocument
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class TechcrunchSpider(CrawlSpider):
    db = MongoDBClient('techcrunch')
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["http://techcrunch.com/"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[contains(@class, 'read-more')]")), callback='parse_1',
             follow=True),
    )

    crawledKeywords = defaultdict(list)

    # if used, the rule doesnt work?
    def parse_0(self, response):
        titles = response.selector.xpath("//li[contains(@class, 'river-block')]")
        for title in titles:
            print title.xpath('@data-sharetitle').extract()

    def parse_1(self, response):
        # TODO: caching titles not to check in db each time
        art_date = response.selector.xpath("//div[contains(@class, 'title-left')]//time/@datetime")
        title = response.selector.xpath("//header[contains(@class, 'article-header')]//h1/text()")
        articles = response.selector.xpath("//div[contains(@class, 'article-entry')]")
        # for article in articles:
        article = articles[0]

        dt = datetime.now()
        date_crawled = str(date(dt.year, dt.month, dt.day))

        # keywords
        # TODO: better text extracting
        # self.html_decode()
        extract = article.extract().split()  # article.re("<([A-Za-z][A-Za-z0-9]*)\\b[^>]*>(.*?)</\\1>")
        # todo to analyse, extract it manually or use a lib?

        # url
        url = str(response.url)

        # title
        title = title.extract()[0]

        if self.isArticleUnique(url):

            _id = self.insertJson({"date_crawled": date_crawled,
                                   "title": title,
                                   "url": url,
                                   # "keywords": extract,
                                   # for other crawlers
                                   # datetime.datetime.strptime('2015-12-31', "%Y-%m-%d").date().isoformat()
                                   # "art_date": art_date.extract()[0]
                                   })

            # TODO optimise
            # is this really one thread? :(
            for word in extract:
                if str(_id) not in self.crawledKeywords[word]:
                    self.crawledKeywords[word].append(str(_id))

    def closed(self, reason):
        for keyword, references in self.crawledKeywords.iteritems():  # self.crawledKeywords:
            self.db.collection.find_one_and_update(
                {"keyword": keyword},
                {"$push": {"references": {'$each': references}}},
                projection={'_id': True},
                upsert=True,
                return_document=ReturnDocument.AFTER
            )

    def find(self, data):
        self.db.collection.find_one(data)

    def insertJson(self, data):
        return self.db.collection.insert(data)

    def isArticleUnique(self, url):
        if self.db.collection.find_one({"url": url}):  # TODO limit to last 10 arts?
            return False
        return True

    def html_decode(self, s):
        """
        Returns the ASCII decoded version of the given HTML string. This does
        NOT remove normal HTML tags like <p>.
        """
        htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;'),
            ('"', '\u201d'),
            ('\'', '\u2019'),

        )
        for code in htmlCodes:
            s = s.replace(code[1], code[0])
        return s
