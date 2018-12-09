# -*- coding: utf-8 -*-
import scrapy

class ScrapinghubSpider(scrapy.Spider):
    name = 'mlmasterytake1'
    allowed_domains = ['machinelearningmastery.com']
    start_urls = ['https://machinelearningmastery.com/blog/']

    # Setting up for the JSON output file
    custom_settings = {
        'FEED_URI' : 'mlmasterytake1.json'
    }

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for blog in response.css('article'):
            item = {
                'blog_title': blog.css('header > h2 > a::text').extract_first(),
                'blog_url': blog.css('header > h2 > a::attr(href)').extract_first(),
                'date': blog.css('div.post-meta > abbr::text').extract_first(),
                'author': blog.css('div.post-meta > span > span.fn > a::text').extract_first(),
                'summary': blog.css('section > p::text').extract_first(),
            }
            yield item

        # follow pagination link
        next_page_url = response.css('div.pagination > a.next').xpath('@href').extract_first()
        if next_page_url:
            self.log('Moving on to next page: ' + next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
