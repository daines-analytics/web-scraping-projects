import scrapy

class DainesBlogSpider(scrapy.Spider):
    name = "mlmasterytake2"
    allowed_domains = ['machinelearningmastery.com']
    api_url = 'https://machinelearningmastery.com/feed/?paged={}'
    pageNum = 1
    start_urls = [api_url.format(pageNum)]

    # Setting up for the JSON output file
    custom_settings = {
        'FEED_URI' : 'mlmasterytake2.json'
    }

    def parse(self, response):
        pageTitle = response.xpath('//channel/title/text()').extract_first()
        self.log(pageTitle)
        if "Page not found" not in pageTitle :
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

            # Follow the pagination links
            self.pageNum += 1
            yield scrapy.Request(url=self.api_url.format(self.pageNum), callback=self.parse)
