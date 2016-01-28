# -*- coding: utf-8 -*-
from collections import defaultdict
from datetime import datetime, date

import scrapy
from crawler.db import MongoDBClient
from pymongo import ReturnDocument
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


#TODO DIFFER COLLECTIONS
class TheVergeSpider(CrawlSpider):
    db = MongoDBClient('techcrunch')
    name = "theverge"
    allowed_domains = ["theverge.com"]
    start_urls = ["http://www.theverge.com"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths="//div[contains(@class, 'm-hero__slot')]"),
             process_request='add_headers', callback='parse_this_shit', follow=False), #process_request='add_headers',
    )

    crawledKeywords = defaultdict(list)

    def start_requests(self):
        requests = []
        for item in self.start_urls:
            requests.append(Request(url=item, headers= {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Chrome/47.0.2526.73 Safari/537.36",
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding":"gzip, deflate, sdch",
                    "Accept-Language":"en-US,en;q=0.8",
                    "Cache-Control":"no-cache",
                    "Connection":"keep-alive",
                    "Cookie":"umbel_api_key=lrjhazrpqbgtnrij; __qca=P0-259424007-1451551704543; chorus_optimize_tracker_id=a662305e-98c4-4d89-b834-4499af9bcf78; krg_uid=%7B%22v%22%3A%2233a666238e7371427dc0fb3de9054fd5%22%7D; __gads=ID=7159254dd24b8b89:T=1451551705:S=ALNI_MZAFLYx56yl5UMsXILVo83kIiPfQg; _cb_ls=1; umbel1-v0=app.user_agent%3DMozilla%252F5.0%2520%28X11%253B%2520Linux%2520x86_64%29%2520AppleWebKit%252F537.36%2520%28KHTML%252C%2520like%2520Gecko%29%2520Ubuntu%2520Chromium%252F47.0.2526.73%2520Chrome%252F47.0.2526.73%2520Safari%252F537.36; OX_plg=swf|shk|pm; chorus_beacon=a485abd3-6472-43ec-81a4-b888e9136662; krg_uidr=%7B%22v%22%3A%2233a666238e7371427dc0fb3de9054fd5%22%2C%22exp%22%3A1453996530511%7D; umbel_api_key=lrjhazrpqbgtnrij; _dc_gtm_UA-26533115-1=1; _gat_UA-26533115-1=1; chorus_optimize_first_clicked_94750088=h:-1060420350 h:-1060420350 http://www.theverge.com/2016/1/27/10841138/uber-lyft-drivers-settlement-class-action-lawsuit-California; chorus_optimize_last_clicked_94750088=h:-1060420350 h:-1060420350 http://www.theverge.com/2016/1/27/10841138/uber-lyft-drivers-settlement-class-action-lawsuit-California; chorus_optimize_conversion_queue=; umbel_browser_id=f6a0b1c6-c02b-455d-97df-7da72da0c0ed; __ybotb=1549; __ybotu=iiu0empetxyhdrucgx; __ybotv=1453919448580; __ybots=ijx63k46hr6nvz0skn.0.ijx63mdg1duiab025w.2; OX_sd=2; __ybota=; __ybote=; __ybotz=; __ybotc=http%3A//ads-adseast.yldbt.com/m/; chorus_optimize_depth3=47 1940378773; chorus_optimize_session=control 0  views 1  root_views 0; _chartbeat2=D6L8yeDRk1YRBeSZT8.1451551709354.1453919452716.0000000000000001; _ga=GA1.2.1966588548.1451551705",
                    "Host":"www.theverge.com",
                    "Pragma":"no-cache",
                    "Referer":"http://www.theverge.com/",
                    "Upgrade-Insecure-Requests":"1"
                 },
            ))
        return requests

    def add_headers(self, request):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/47.0.2526.73 Chrome/47.0.2526.73 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate, sdch",
            "Accept-Language":"en-US,en;q=0.8",
            "Cache-Control":"no-cache",
            "Connection":"keep-alive",
            "Cookie":"umbel_api_key=lrjhazrpqbgtnrij; __qca=P0-259424007-1451551704543; chorus_optimize_tracker_id=a662305e-98c4-4d89-b834-4499af9bcf78; krg_uid=%7B%22v%22%3A%2233a666238e7371427dc0fb3de9054fd5%22%7D; __gads=ID=7159254dd24b8b89:T=1451551705:S=ALNI_MZAFLYx56yl5UMsXILVo83kIiPfQg; _cb_ls=1; umbel1-v0=app.user_agent%3DMozilla%252F5.0%2520%28X11%253B%2520Linux%2520x86_64%29%2520AppleWebKit%252F537.36%2520%28KHTML%252C%2520like%2520Gecko%29%2520Ubuntu%2520Chromium%252F47.0.2526.73%2520Chrome%252F47.0.2526.73%2520Safari%252F537.36; OX_plg=swf|shk|pm; chorus_beacon=a485abd3-6472-43ec-81a4-b888e9136662; krg_uidr=%7B%22v%22%3A%2233a666238e7371427dc0fb3de9054fd5%22%2C%22exp%22%3A1453996530511%7D; umbel_api_key=lrjhazrpqbgtnrij; _dc_gtm_UA-26533115-1=1; _gat_UA-26533115-1=1; chorus_optimize_first_clicked_94750088=h:-1060420350 h:-1060420350 http://www.theverge.com/2016/1/27/10841138/uber-lyft-drivers-settlement-class-action-lawsuit-California; chorus_optimize_last_clicked_94750088=h:-1060420350 h:-1060420350 http://www.theverge.com/2016/1/27/10841138/uber-lyft-drivers-settlement-class-action-lawsuit-California; chorus_optimize_conversion_queue=; umbel_browser_id=f6a0b1c6-c02b-455d-97df-7da72da0c0ed; __ybotb=1549; __ybotu=iiu0empetxyhdrucgx; __ybotv=1453919448580; __ybots=ijx63k46hr6nvz0skn.0.ijx63mdg1duiab025w.2; OX_sd=2; __ybota=; __ybote=; __ybotz=; __ybotc=http%3A//ads-adseast.yldbt.com/m/; chorus_optimize_depth3=47 1940378773; chorus_optimize_session=control 0  views 1  root_views 0; _chartbeat2=D6L8yeDRk1YRBeSZT8.1451551709354.1453919452716.0000000000000001; _ga=GA1.2.1966588548.1451551705",
            "Host":"www.theverge.com",
            "Pragma":"no-cache",
            "Referer":"http://www.theverge.com/",
            "Upgrade-Insecure-Requests":"1"
        }
        return Request(request.url, headers=headers)

    def parse_this_shit(self, response):
        print '--------------------------------------------  parsing 1 -------------------------------------------- '
        # TODO: caching titles not to check in db each time
        #art_date = response.selector.xpath("//div[contains(@class, 'title-left')]//time/@datetime")
        #title = response.selector.xpath("//header[contains(@class, 'article-header')]//h1/text()")
        # for article in articles:
        #<article class="m-entry m-article">
        articles = response.selector.xpath("//article[contains(@class, 'm-article')]")

        print articles.extract()

    def closed(self, reason):
        print '--------------------------------------------  closed   -------------------------------------------- '