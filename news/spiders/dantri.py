import re
from news_crawler.spiders.base import BaseCrawler


class DantriCrawler(BaseCrawler):
    cate_list = ["su-kien", "xa-hoi"]

    def __init__(self, cate, link, limit_articles):
        super().__init__("dantri", cate, link, limit_articles)

    def gen_link(cate):
        return f"https://dantri.com.vn/{cate}"

    def extract_data_from_response(self):
        news_list = self.response.css("div.clearfix").css("div.news-item")

        for news in news_list:
            path = news.css(" ::attr(href)").get()
            title = news.css("h3.news-item__title ::text").getall()
            title = "".join(title).strip()

            link = "https://dantri.com.vn/" + path
            if link not in self.visited_links:
                self.visited_links.append(link)
                self.fetch_link(link)

                content = "".join(self.response.css("div.dt-news__content").css("p ::text").getall())
                content = "".join(content).replace("\r", "")
                content = re.sub("\n+", "\n", content).strip()

                if title == "" or content == "" or link == "":
                    continue

                article = {"title": "", "content": "", "link": ""}
                article["title"] = title
                article["content"] = content
                article["link"] = link
                self.data.append(article)
                if len(self.data) == self.limit_articles:
                    break
