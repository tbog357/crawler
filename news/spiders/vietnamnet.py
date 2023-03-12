from news_crawler.spiders.base import BaseCrawler
import json


class VietnamnetCrawler(BaseCrawler):
    cate_list = ["thoi-su", "kinh-doanh"]

    def __init__(self, cate, link, limit_articles):
        super().__init__("vietnamnet", cate, link, limit_articles)

    def gen_link(self, cate):
        return "https://vietnamnet.vn/jsx/loadmore/?domain=desktop&c={}&p=1&s=15&a=5".format(cate)

    def extract_data_from_response(self):
        list_news = json.loads(self.response.css(" ::text").get()[8:])

        for new in list_news:
            title = new["title"]
            link = new["link"]
            if link not in self.visited_links:
                self.visited_links.append(link)
                self.fetch_link(link)
                content = self.response.css("#ArticleContent").css("p ::text").getall()
                content = "".join(content)

                if title == "" or content == "" or link == "":
                    continue
                article = {"title": "", "content": "", "link": ""}
                article["title"] = title
                article["content"] = content
                article["link"] = link
                self.data.append(article)

                if len(self.data) == self.limit_articles:
                    break
