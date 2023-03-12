import requests
from scrapy.http import TextResponse
import re
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures

vnexpress_categories = []
# ['giao-duc', 'doi-song', 'du-lich',  'kinh-doanh', 'suc-khoe']
links = []
def crawler(cate, num_articles):
    r = requests.get('https://vnexpress.net/' + cate)
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    news = response.css("div.col-left.col-small").css("article")
    
    data = []
    
    for new in news:
        title = new.css("h3.title-news").css("a ::text").get()
        if title == None:
            continue
        link = new.css("h3.title-news").css("a ::attr(href)").get()
        if link not in links:
            r_content = requests.get(link)
            r_content = TextResponse(r_content.url, body=r_content.text, encoding='utf-8')
            content = r_content.css("article.fck_detail").css("p ::text").getall()
            title = title.strip()
            content = " ".join(content)
            # print(title)
            # print(content)
            # print(link)
            # print()
            if title == "" or content == "" or link == "":
                continue            
            
            article = {"title": "", "content": "", "link": ""}
            article["title"] = title
            article["content"] = content
            article["link"] = link
            data.append(article)       
            if len(data) == num_articles:
                break
    with open("data/vnexpress_{}".format(cate), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)     
        
if __name__ == "__main__":
    t0 = time.time()
    threads = []
    for cate in vnexpress_categories:
        t = threading.Thread(target=crawler, args=(cate, 10, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Done in: ", time.time() - t0)   