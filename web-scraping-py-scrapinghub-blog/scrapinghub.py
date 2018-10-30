# -*- coding: utf-8 -*-
import scrapy


class ScrapinghubSpider(scrapy.Spider):
    name = 'scrapinghub'
    allowed_domains = ['scrapinghub.com']
    start_urls = ['https://blog.scrapinghub.com/']

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        for blog in response.css('div.post-item'):
            item = {
                'blog_title': blog.css('div.post-header > h2 > a::text').extract_first(),
                'blog_url': blog.css('div.post-header > h2 > a::attr(href)').extract_first(),
                'date': blog.css('div.post-header > div.byline > span.date > a::text').extract_first(),
                'author': blog.css('div.post-header > div.byline > span.author > a::text').extract_first(),
                'summary': blog.css('div.post-content > p::text').extract_first(),
            }
            yield item

        # follow pagination link
        next_page_url = response.css('div.blog-pagination > a.next-posts-link').xpath('@href').extract_first()
        if next_page_url:
#            next_page_url = response.urljoin(next_page_url)
            self.log('Moving on to next page: ' + next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
