# -*- coding: utf-8 -*-
import scrapy


class ListdatasetsSpider(scrapy.Spider):
    name = 'listdatasets'
    start_urls = ['https://registry.opendata.aws/']

    def parse(self, response):
        for dataset in response.css('div.dataset'):
            item = {
                'dataset_name': dataset.css('h3 > a::text').extract_first(),
                'detail_url': response.urljoin(dataset.css('h3 > a::attr(href)').extract_first()),
                'tags': dataset.css('p > span::text').extract(),
                'description': dataset.css('p')[1].extract(),
            }
            yield item
