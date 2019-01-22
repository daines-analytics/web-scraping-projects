import scrapy

class DainesBlogSpider(scrapy.Spider):
    name = "merelydoitblog"
    allowed_domains = ['merelydoit.blog']
    api_url = 'https://merelydoit.blog/feed/?paged={}'
    pageNum = 1
    start_urls = [api_url.format(pageNum)]

    # Setting up for the JSON output file
    custom_settings = {
        'FEED_URI' : 'merelydoitblog.json'
    }

    def parse(self, response):
        pageTitle = response.xpath('//channel/title/text()').extract_first()
        self.log(pageTitle)
        if "Page not found" not in pageTitle :
            self.log('I just visited: ' + response.url)

            # Remove the XML namespaces
            response.selector.remove_namespaces()

            # Extract article information
            title = response.xpath('//item/title/text()').extract()
            author = response.xpath('//item/creator/text()').extract()
            post_date = response.xpath('//item/pubDate/text()').extract()
            link_url = response.xpath('//item/link/text()').extract()
            blog_text = response.xpath('//item/description/text()').extract()

            for item in zip(title, author, post_date, link_url, blog_text):
                scraped_info = {
                    'Title' : item[0],
                    'Author' : item[1],
                    'Post_Date' : item[2],
                    'Link_URL' : item[3],
                    'Blog_Text' : item[4]
                }
                yield scraped_info

            # Follow the pagination links
            self.pageNum += 1
            yield scrapy.Request(url=self.api_url.format(self.pageNum), callback=self.parse)
