import requests
from scrapy.http import TextResponse
import re
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures

nhandan_categories = ['kinhte', 'xahoi']
links = []
def crawler(cate, num_articles):
    r = requests.get('https://nhandan.com.vn/' + cate)
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    list_news = response.css("article").css("div.box-title")
    
    data = []
    for new in list_news:
        title = new.css("a ::text").get()
        link = new.css("a ::attr(href)").get()
        link = 'https://nhandan.com.vn/' + link
        if link not in links:
            links.append(link)
            r_content = requests.get(link)
            r_content = TextResponse(r_content.url, body=r_content.text, encoding='utf-8')
            content = r_content.css("div.detail-content-body ::text").getall()
            content = " ".join(content)
            content = strip_multiple_whitespaces(content)
            if title == "" or content == "" or link == "":
                continue
            article = {"title": "", "content": "", "link": ""}
            article["title"] = title
            article["content"] = content
            article["link"] = link
            data.append(article)  
            if len(data) == num_articles:
                break
    with open("data/nhandan_{}".format(cate), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)      
        # print(title)
        # print(content)
        # print(link)
        # print()
        
if __name__ == "__main__":
    t0 = time.time()
    threads = []
    for cate in nhandan_categories:
        t = threading.Thread(target=crawler, args=(cate, 10, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Done in: ", time.time() - t0)  