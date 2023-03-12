import time
import scrapy
import logging
from scrapy_selenium.http import SeleniumRequest
from scrapy.selector import Selector


class NewsSpider(scrapy.Spider):
    name = 'news'
    # allowed_domains = ['cafef.vn']
    # start_urls = ['http://cafef.vn/thi-truong-chung-khoan.chn']

    def start_requests(self):
        yield SeleniumRequest(
            url='http://cafef.vn/thi-truong-chung-khoan.chn',
            wait_time=1,
            callback=self.parse
        )

    def parse(self, response):

        # Deal with content loaded 
        driver = response.meta["driver"]

        while  len(driver.find_elements_by_xpath("//a[@title='Xem thêm']")) != 1:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
        time.sleep(3)

        
        response_obj = Selector(text=driver.page_source)

        for new in response_obj.xpath("//h3/a"):
            title = new.xpath(".//text()").get()
            link = new.xpath(".//@href").get()

            link = response.urljoin(link)
            yield response.follow(
                url = link,
                callback=self.parse_content,
                meta = {
                    "title": title,
                    "link": link
                }
            )

    def parse_content(self, response):
        # print(response.resquest.headers["User-Agent"])
        # Get tile and link 
        title = response.request.meta["title"]
        link = response.request.meta["link"]
        
        # Date
        date = response.xpath("normalize-space(.//span[@class='pdate']/text())").get()

        # Description 
        description = response.xpath("normalize-space(.//h2[@class='sapo']/text())").get()

        # Main content
        content = ""
        for p in response.xpath(".//span[@id='mainContent']/p"):
            content += p.xpath("normalize-space(.//text())").get() + " "

        # Source 
        yield {
            "title": title,
            "link": link,
            "date": date,
            "description": description,
            "content": content,
            "author": response.xpath(".//p[@class='author']/text()").get(),
            "source": response.xpath(".//p[@class='source']/text()").get(),
        }   
        
