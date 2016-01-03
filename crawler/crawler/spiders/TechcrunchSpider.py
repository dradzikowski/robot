# -*- coding: utf-8 -*-
from datetime import datetime, date
from crawler.db import MongoDBClient
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

    # if used the rule doesnt work?
    def parse_0(self, response):
        titles = response.selector.xpath("//li[contains(@class, 'river-block')]")
        for title in titles:
            self.print_sep()
            print title.xpath('@data-sharetitle').extract()
            self.print_sep()

    def parse_1(self, response):
        #TODO: caching titles not to check in db each time
        art_date = response.selector.xpath("//div[contains(@class, 'title-left')]//time/@datetime")
        title = response.selector.xpath("//header[contains(@class, 'article-header')]//h1/text()")
        articles = response.selector.xpath("//div[contains(@class, 'article-entry')]")
        for article in articles:
            # date crawled
            dt = datetime.now()
            date_crawled = str(date(dt.year, dt.month, dt.day))

            # keywords
            # TODO: better text extracting
            extract = self.html_decode(article.extract()).split()

            # url
            url = str(response.url)

            # title
            title = title.extract()[0]

            if (self.isArticleUnique(url)):
                self.insertJson({"date_crawled": date_crawled,
                                 "title": title,
                                 "url": url,
                                 "keywords": extract,
                                 #for other crawlers
                                 #datetime.datetime.strptime('2015-12-31', "%Y-%m-%d").date().isoformat()
                                 "art_date": art_date.extract()[0]
                                 })

    def insertJson(self, data):
        self.db.collection.insert_one(data)

    def isArticleUnique(self, url):
        if self.db.collection.find_one({"url": url}):  # TODO limit to last 10 arts
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
