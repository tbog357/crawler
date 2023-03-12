import scrapy
import time
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector

class PriceSpider(scrapy.Spider):
    name = 'price'
    # allowed_domains = ['iboard.ssi.com.vn/bang-gia/vn30']
    # start_urls = ['https://iboard.ssi.com.vn/bang-gia/vn30']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://iboard.ssi.com.vn/bang-gia/vn30",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta["driver"]
        time.sleep(2)
        response_obj = Selector(text=driver.page_source)

        for stock in response_obj.xpath("//tbody[@class='table-body']/tr")[:-1]:
            code = stock.xpath(".//@id").get()
            name = stock.xpath("(.//td)[1]/@data-tooltip").get()

            yield {
                "code": code,
                "name": name
            }
