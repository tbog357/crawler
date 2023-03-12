import scrapy


class BestsellersSpider(scrapy.Spider):
    name = 'bestsellers'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        for product in response.xpath("//div[@id='product-lists']/div"):
            yield {
                "url": product.xpath(".//div[@class='product-img-outer']/a/@href").get(),
                "image_link": product.xpath(".//img[@class='lazy d-block w-100 product-img-default']/@data-src").get(),
                "name": product.xpath("normalize-space(.//div[@class='p-title']/a/text())").get(),
                "price": product.xpath(".//div[@class='p-price']//span/text()").get(),
            }
        
        next_page = response.xpath("//ul[@class='pagination']/li[position() = last()]/a/@href").get()
        print("NEXT_PAGE", next_page)
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)