import re
import requests
from scrapy.http import TextResponse
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures


dantri_categories = ['su-kien', 'xa-hoi']
links = []
def crawler(cate, num_articles):
    r = requests.get('https://dantri.com.vn/' + cate + '.htm')
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    new_list = response.css('div.clearfix').css('div.news-item')
    data = []
    
    for new in new_list:
        link = new.css(" ::attr(href)").get()
        title = new.css("h3.news-item__title ::text").getall()
        title = ''.join(title).strip()
        
        link = 'https://dantri.com.vn/' + link
        if link not in links:
            links.append(link)
            r_content = requests.get(link)
            r_content = TextResponse(r_content.url, body=r_content.text, encoding='utf-8')
            
            content = ''.join(r_content.css("div.dt-news__content").css("p ::text").getall())
            content = ''.join(content).replace('\r', '')
            content = re.sub('\n+', '\n', content).strip()
            
            if title == "" or content == "" or link == "":
                continue
            
            article = {"title": "", "content": "", "link": ""}
            article["title"] = title
            article["content"] = content
            article["link"] = link
            data.append(article)
            if len(data) == num_articles:
                break
            
    with open("data/dantri_{}".format(cate), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    t0 = time.time()
    threads = []
    for cate in dantri_categories:
        t = threading.Thread(target=crawler, args=(cate, 10, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Done in: ", time.time() - t0)