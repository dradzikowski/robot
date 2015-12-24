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
        titles = response.selector.xpath("//div[contains(@class, 'article-entry')]")
        for title in titles:
            #title.xpath('//p').extract()
            self.print_sep()
            #print title.extract().split()
            dt = datetime.now()

            #self.insertKeyValue(str(date(dt.year, dt.month, dt.day)), title.extract().split())

            date_crawled = str(date(dt.year, dt.month, dt.day))
            extract = title.extract().split()
            url = str(response.url)

            self.insertJson({"date":date_crawled, "url": url, "keywords": extract})
            #self.print_sep()

    def generate_date_key(self):
        return string.replace(str(datetime.now()), '.', ':')

    def make_key(self, to_be_key):
        return string.replace(str(to_be_key), '.', ':')

    def insertKeyValue(self, key, value):
        self.db.collection.insert_one({key: value})

    def insertJson(self, data):
        self.db.collection.insert_one(data)

    def print_sep(self):
        print "___________________________________________________________________________"

    # titles.xpath("a/text()").extract()
    # titles.xpath("a/@href").extract()
