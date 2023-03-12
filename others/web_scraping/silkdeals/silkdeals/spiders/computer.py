import scrapy
from scrapy_selenium import SeleniumRequest

class ComputerSpider(scrapy.Spider):
    name = 'computer'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://slickdeals.net/computer-deals/",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        pass
