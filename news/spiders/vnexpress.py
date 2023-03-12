from news_crawler.spiders.base import BaseCrawler

class Vnexpress1Crawler(BaseCrawler):
    cate_list = ["giao-duc", "doi-song", "du-lich", "kinh-doanh", "suc-khoe"]

    def __init__(self, cate, link, limit_articles):
        super().__init__("vnexpress", cate, link, limit_articles)

    def gen_link(cate):
        return "https://vnexpress.net/" + cate

    def extract_data_from_response(self):
        news = self.response.css("div.col-left.col-small").css("article")

        for new in news:
            title = new.css("h3.title-news").css("a ::text").get()
            if title == None:
                continue
            link = new.css("h3.title-news").css("a ::attr(href)").get()
            if link not in self.visited_links:
                self.fetch_link(link)
                content = self.response.css("article.fck_detail").css("p ::text").getall()
                title = title.strip()
                content = " ".join(content)

                if title == "" or content == "" or link == "":
                    continue

                article = {"title": "", "content": "", "link": ""}
                article["title"] = title
                article["content"] = content
                article["link"] = link
                self.data.append(article)
                if len(self.data) == self.limit_articles:
                    break


class Vnexpress2Crawler(BaseCrawler):
    cate_list = ["thoi-su", "kinh-doanh", "tin-xem-nhieu"]

    def __init__(self, cate, link, limit_articles):
        super().__init__("vnexpress", cate, link, limit_articles)

    def gen_link(cate):
        return "https://vnexpress.net/" + cate

    def extract_data_from_response(self):
        news = self.response.css("div.width_common.list-news-subfolder").css("article")
        for new in news:
            title = new.css("h3.title-news ::text").getall()
            link = new.css("h3.title-news ::attr(href)").get()

            if link not in self.visited_links and link is not None:
                self.visited_links.append(link)
                self.fetch_link(link)
                content = self.response.css("article.fck_detail").css("p ::text").getall()
                title = " ".join(title).strip()
                content = " ".join(content).strip()

                if title == "" or content == "" or link == "":
                    continue

                article = {"title": "", "content": "", "link": ""}
                article["title"] = title
                article["content"] = content
                article["link"] = link
                self.data.append(article)
                if len(self.data) == self.limit_articles:
                    break
