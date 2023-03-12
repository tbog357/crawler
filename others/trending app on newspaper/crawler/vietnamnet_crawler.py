import requests
from scrapy.http import TextResponse
import re
import json
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures

vietnamnet_categories = ['thoi-su', 'kinh-doanh']
links = []
def crawler(cate, num_articles):
    r = requests.get('https://vietnamnet.vn/jsx/loadmore/?domain=desktop&c={}&p=1&s=15&a=5'.format(cate))
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    list_news = json.loads(response.css(" ::text").get()[8:])
    
    data = []
    
    for new in list_news:
        title = new['title']
        link = new['link']
        if link not in links:
            links.append(link)
            r_content = requests.get(link)
            r_content = TextResponse(r_content.url, body=r_content.text, encoding='utf-8')
            
            content = r_content.css("#ArticleContent").css("p ::text").getall()
            content = ''.join(content)
            # print(title)
            # print(content)
            # print(link_content)
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
        
    with open("data/vietnamnet_{}".format(cate), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
if __name__ == "__main__":
    t0 = time.time()
    threads = []
    for cate in vietnamnet_categories:
        t = threading.Thread(target=crawler, args=(cate, 10, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Done in: ", time.time() - t0)