import re
from news_crawler.spiders.base import BaseCrawler
from gensim.parsing.preprocessing import strip_multiple_whitespaces


class ThanhnienCrawler(BaseCrawler):
    cate_list = ["thoi-su", "tai-chinh-kinh-doanh"]

    def gen_link(cate):
        return "https://thanhnien.vn/" + cate + "/"

    def extract_data_from_response(self):
        articles = self.response.css("div.feature").css("article")

        for article in articles:
            title = article.css("a.story__title::text").get().strip()
            path = article.css("a::attr(href)").get()
            link = "https://thanhnien.vn/" + path

            self.fetch_link(link)
            body = self.response.css("div.l-content")
            raw_content = body.css("div#abody.cms-body.detail ::text").getall()

            trash = body.css("div#abody.cms-body.detail").css(".video ::text").getall()
            trash += body.css("div#abody.cms-body.detail").css("script ::text").getall()
            trash += body.css("div#abody.cms-body.detail").css("table ::text").getall()

            clean_text = []
            for text in raw_content:
                if text in trash:
                    pass
                else:
                    clean_text.append(text)

            content = "".join(clean_text).replace("\r", "")
            content = re.sub("\n+", "\n", content).strip()
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
