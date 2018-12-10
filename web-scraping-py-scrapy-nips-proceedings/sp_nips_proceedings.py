import scrapy
import os
import urllib.request
import shutil

class NIPSSpider(scrapy.Spider):
    name = 'nipsproceedings'
    start_urls = ['https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017']

    # Setting up for the JSON output file
    custom_settings = {
        'FEED_URI' : 'nipsproceedings-scrapy.json'
    }

    def parse(self, response):
        self.log('I just visited: ' + response.url)
        website_url = "https://papers.nips.cc"
        for doc_entry in response.css('div.main ul li'):
            item = {
                'title': doc_entry.css('a::text').extract_first(),
                'authors': doc_entry.css('a.author::text').extract(),
                'doc_link': website_url + doc_entry.css('a::attr(href)').extract_first(),
            }
            yield item

            next_url = item['doc_link']
            self.log('About to visit: ' + next_url)
            # follow links to the individual document page
            yield scrapy.Request(next_url, self.parse_doc)

    def parse_doc(self, response):
        self.log('Visiting doc URL: ' + response.url)
        website_url = "https://papers.nips.cc"
        for artifact in response.css('div.main a'):
            if artifact.css('a::text').extract_first() == "[PDF]":
                doc_path = website_url + artifact.css('a::attr(href)').extract_first()
                dest_file = os.path.basename(doc_path)
                self.log('Grabing document: ' + doc_path + " as " + dest_file)
                with urllib.request.urlopen(doc_path) as in_resp, open(dest_file, 'wb') as out_file:
                    shutil.copyfileobj(in_resp, out_file)
