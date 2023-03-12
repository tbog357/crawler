import requests
from scrapy.http import TextResponse
import re
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures

thanhnien_categories = ['thoi-su', 'tai-chinh-kinh-doanh']

def crawler(cate, num_articles):
    r = requests.get('https://thanhnien.vn/' + cate + "/")
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    articles = response.css('div.feature').css('article')
    
    data = []
    
    for article in articles:
        title = article.css("a.story__title::text").get().strip()
        # print(title)
        link = article.css("a::attr(href)").get()
        link = 'https://thanhnien.vn/'+ link
        r_content = requests.get(link)
        r_content = TextResponse(r_content.url, body=r_content.text, encoding='utf-8')
        body = r_content.css("div.l-content")
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
                
        content = ''.join(clean_text).replace('\r', '')
        content = re.sub('\n+', '\n', content).strip()
        content = strip_multiple_whitespaces(content)
        # print(title)
        # print(content)
        # print(link)
        if title == "" or content == "" or link == "":
            continue
        article = {"title": "", "content": "", "link": ""}
        article["title"] = title
        article["content"] = content
        article["link"] = link
        data.append(article)
        
        if len(data) == num_articles:
            break
    with open("data/thanhnien_{}".format(cate), "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)        
        
if __name__ == "__main__":
    t0 = time.time()
    threads = []
    for cate in thanhnien_categories:
        t = threading.Thread(target=crawler, args=(cate, 10, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("Done in: ", time.time() - t0)