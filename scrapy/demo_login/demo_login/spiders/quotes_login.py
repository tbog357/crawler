import scrapy
from scrapy import FormRequest

class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']

    def parse(self, response):
        crsf_token = response.xpath("//input[@class='crsf_token']/@value").get()
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'crsf_token':crsf_token,
                'username': 'admin',
                'password': 'admin'
                },
            callback=self.after_login
        )
    
    def after_login(self, response):
        if response.xpath("//a[@href='/logout']/text()").get():
            print("logged in")