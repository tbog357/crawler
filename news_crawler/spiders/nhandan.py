from news_crawler.spiders.base import BaseCrawler
from gensim.parsing.preprocessing import strip_multiple_whitespaces


class NhandanCrawler(BaseCrawler):
    cate_list = ["kinhte", "xahoi"]

    def __init__(self, cate, link, limit_articles):
        super().__init__("nhandan", cate, link, limit_articles)
        self.visited_links = []

    def gen_link(cate):
        return f"https://nhandan.com.vn/{cate}"

    def extract_data_from_response(self):
        list_news = self.response.css("article").css("div.box-title")

        for new in list_news:
            title = new.css("a ::text").get()
            link = new.css("a ::attr(href)").get()
            link = "https://nhandan.com.vn/" + link
            if link not in self.visited_links:
                self.visited_links.append(link)
                self.fetch_link(link)
                content = self.response.css("div.detail-content-body ::text").getall()
                content = " ".join(content)
                content = strip_multiple_whitespaces(content)
                if title == "" or content == "" or link == "":
                    continue
                article = {"title": "", "content": "", "link": ""}
                article["title"] = title
                article["content"] = content
                article["link"] = link
                self.data.append(article)
                if len(self.data) == self.limit_articles:
                    break
