import requests
from scrapy.http import TextResponse
import re
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures


def crawler(num_articles):
    r = requests.get("https://vnexpress.net/tin-xem-nhieu")
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    list_news = response.css("div.width_common.list-news-subfolder").css("article")
    data = []
    for new in list_news:
        title = new.css("h3.title-news ::text").getall()
        title = " ".join(title).strip()
        
        link = new.css("h3.title-news ::attr(href)").get()
        
        
        if title == "":
            continue
            
        r_content = requests.get(link)
        r_content = TextResponse(r_content.url, body=r_content.text, encoding='utf-8')
        content = r_content.css("article.fck_detail").css("p ::text").getall()
        content = " ".join(content).strip()
        article = {"title": "", "content": "", "link": ""}
        article["title"] = title
        article["content"] = content
        article["link"] = link
        data.append(article)       
        if len(data) == num_articles:
            break        
    with open("data/vnexpress_most_view", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)   
        # print(title)
        # print(content)
        # print(link)
        # print()
if __name__ == "__main__":
    t0 = time.time()
    crawler(40)
    print("Done in: ", time.time() - t0)  