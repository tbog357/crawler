import requests
from scrapy.http import TextResponse
import re
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures

laodong_categories = ['thoi-su', 'xa-hoi']
links = []

def crawler(cate, num_articles):
    r = requests.get('https://laodong.vn/' + cate + '/')
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    
    data = []
    for new in response.css("#category_main_content > ul:nth-child(1)").css("li"):
        title = new.css("h4 ::text").get()
        link = new.css("a ::attr(href)").get()
        if link not in links:
            # print(link)
            links.append(link)
            r_content = requests.get(link)
            r_content = TextResponse(r_content.url, body=r_content.text, encoding='utf-8')
            content = r_content.css("div.left-sidebar.row > div.articleCon > div > div.wrapper-main-content > article > div.article-content ::text").getall()
            content = ''.join(content).replace('\r', '')
            content = re.sub('\n+', '\n', content).strip()
            if title == "" or content == "" or link == "":
                continue
            # print(title)
            # print(content)
            # print(link)
            article = {"title": "", "content": "", "link": ""}
            article["title"] = title
            article["content"] = content
            article["link"] = link      
            data.append(article)  
            
            if len(data) == num_articles:
                break
            
    with open("data/laodong_{}".format(cate), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    t0 = time.time()
    threads = []
    for cate in laodong_categories:
        t = threading.Thread(target=crawler, args=(cate, 10, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Done in: ", time.time() - t0)