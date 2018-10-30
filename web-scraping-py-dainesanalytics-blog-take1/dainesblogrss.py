# -*- coding: utf-8 -*-
import scrapy

class DainesBlogRSSSpider(scrapy.Spider):
    name = 'dainesblogrss'
    allowed_domains = ['dainesanalytics.blog/feed/']
    start_urls = ['https://dainesanalytics.blog/feed/']

    # Setting up for the JSON output file
    custom_settings = {
        'FEED_URI' : 'dainesblogrss.json'
    }

    def parse(self, response):
        self.log('I just visited: ' + response.url)

        # Remove the XML namespaces
        response.selector.remove_namespaces()

        # Extract article information
        titles = response.xpath('//item/title/text()').extract()
        authors = response.xpath('//item/creator/text()').extract()
        dates = response.xpath('//item/pubDate/text()').extract()
        links = response.xpath('//item/link/text()').extract()
        description = response.xpath('//item/description/text()').extract()

        for item in zip(titles, authors, dates, links, description):
            scraped_info = {
                'Title' : item[0],
                'Author' : item[1],
                'Publish_Date' : item[2],
                'Link' : item[3],
                'Description' : item[4]
            }
            yield scraped_info
