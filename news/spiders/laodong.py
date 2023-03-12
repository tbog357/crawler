import re
from news_crawler.spiders.base import BaseCrawler


class LaodongCrawler(BaseCrawler):
    cate_list = ["thoi-su", "xa-hoi"]

    def __init__(self, cate, link, limit_articles):
        super().__init__("laodong", cate, link, limit_articles)

    def gen_link(cate):
        return f"https://laodong.vn/{cate}"

    def extract_data_from_response(self):
        for new in self.response.css("#category_main_content > ul:nth-child(1)").css("li"):
            title = new.css("h4 ::text").get()
            link = new.css("a ::attr(href)").get()
            if link not in self.visited_links:
                self.visited_links.append(link)
                self.fetch_link(link)
                content = self.response.css(
                    "div.left-sidebar.row > div.articleCon > div > div.wrapper-main-content > article > div.article-content ::text"
                ).getall()
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
