import scrapy
import json

class EbookSpider(scrapy.Spider):
    name = 'ebook'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12&offset=12/']

    def parse(self, response):
        resp = json.loads(response.body)
        ebooks = resp.get('works')
        for ebook in ebooks:
            yield {
                'title': ebook.get('title'),
                'subject': ebook.get('subject'),
            }
