import scrapy


class DebtSpider(scrapy.Spider):
    name = 'debt'
    allowed_domains = ['worldpopulationreview.com/countries/countries-by-national-debt']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        rows = response.xpath("//table[@class='jsx-1487038798 table table-striped tp-table-body']/tbody/tr")
        for row in rows:
            country_name = row.xpath(".//td[1]/a/text()").get()
            gdb_debt = row.xpath(".//td[2]/text()").get()

            yield {
                "country_name": country_name,
                "gdb_dept": gdb_debt,
            }