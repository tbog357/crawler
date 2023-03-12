import scrapy
from scrapy_selenium import SeleniumRequest

class AnkerSpider(scrapy.Spider):
    name = 'anker'
    # allowed_domains = ['www.shopee.vn/shop']
    # start_urls = ['https://shopee.vn/shop/16461019/search']

    def start_requests(self):
        yield SeleniumRequest(
            url="https://shopee.vn/shop/16461019/search",
            wait_time=3
        )

    def parse(self, response):
        with open ("page_source.html", "w") as file:
            file.write(response.body.decode("utf-8"))
        for item in response.xpath("//div[@class='_3EfFTx']"):
            title = item.xpath(".//div[@class='_1NoI8_ A6gE1J _1co5xN']/text()").get()
            prices = item.xpath(".//div[@class='QmqjGn']")

            all_prices = []
            for price in prices:
                all_prices.append(price.xpath(".//span[@class='_1xk7ak']").get())
            
            yield {
                "title": title,
                "prices": all_prices
            }
