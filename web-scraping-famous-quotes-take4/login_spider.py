import scrapy

class LoginSpider(scrapy.Spider):
    name = "login"
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        # Extract the CSRF token value
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        # Create a Python dictionary with the form values
        data = {
            'csrf_token' : token,
            'username' : 'abc',
            'password' : 'abc',
        }
        # Submit a Post request to login
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_quotes)

    def parse_quotes(self, response):
        # Parse the items on page after login
        self.log('I just visited: ' + response.url)
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'goodreads_url': quote.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first(),
            }
            yield item

        # follow pagination link
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            self.log('Moving on to: ' + next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_quotes)
