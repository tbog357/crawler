import json
import requests
import threading
from scrapy.http import TextResponse

class BaseCrawler(threading.Thread):
    cate_list = None

    def __init__(self, news_site, cate, link, limit_articles):
        super().__init__()
        self.news_site = news_site
        self.cate = cate
        self.link = link
        self.response = None
        self.data = []
        self.limit_articles = limit_articles
        self.visited_links = []

    def gen_link(self, cate):
        pass

    def fetch_link(self, link=None):
        if link is None:
            link = self.link
        response = requests.get(link)
        self.response = TextResponse(url=response.url, body=response.content, encoding='utf-8')

    def extract_data_from_response(self):
        pass

    def save_to_file(self):
        save_path = f"news_data/{self.news_site}_{self.cate}"
        if len(self.data) > 0:
            with open(save_path, "w", encoding="utf-8") as file:
                json.dump(
                    self.data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

    def reset_thread(self):
        self.visited_links = []

    def run(self):
        self.fetch_link()
        self.extract_data_from_response()
        self.save_to_file()
        self.reset_thread()
