# -*- coding: utf-8 -*-
import string

import scrapy
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from crawler.db import MongoDBClient
from datetime import datetime, date


class CragispiderSpider(CrawlSpider):
    db = MongoDBClient('techcrunch')
    name = "techcrunch"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["http://techcrunch.com/"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=("//a[contains(@class, 'read-more')]")), callback='parse_1', follow=True),
    )

    # if used the rule doesnt work?
    def parse_0(self, response):
        titles = response.selector.xpath("//li[contains(@class, 'river-block')]")
        for title in titles:
            self.print_sep()
            print title.xpath('@data-sharetitle').extract()
            self.print_sep()
    #   self.insert(self.generate_date_key(), title.extract().split())

    def parse_1(self, response):
        art_date = response.selector.xpath("//div[contains(@class, 'title-left')]//time/@datetime")
        title = response.selector.xpath("//header[contains(@class, 'article-header')]//h1/text()")
        articles = response.selector.xpath("//div[contains(@class, 'article-entry')]")
        for article in articles:
            #date crawled
            dt = datetime.now()
            date_crawled = str(date(dt.year, dt.month, dt.day))

            #keywords
            extract = self.html_decode(article.extract()).split()

            #url
            url = str(response.url)

            #title
            title = self.html_decode(title.extract()[0])

            self.insertJson({"date_crawled":date_crawled,
                             "title":title,
                             "url": url,
                             "keywords": extract,
                             "art_date":art_date.extract()})

    def insertKeyValue(self, key, value):
        self.db.collection.insert_one({key: value})

    def insertJson(self, data):
        self.db.collection.insert_one(data)

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