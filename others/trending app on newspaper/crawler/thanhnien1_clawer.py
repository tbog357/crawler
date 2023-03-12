import re
import requests
from scrapy.http import TextResponse
from gensim.parsing.preprocessing import strip_multiple_whitespaces

import time
import json
import threading
import concurrent.futures


def crawler(num_articles):
    r = requests.get("https://thanhnien.vn/#sharetab")
    response = TextResponse(r.url, body=r.text, encoding='utf-8')

    list_news = response.css("article.story--text")
    
    data = []
    for new in list_news:
        title = new.css(" ::text").getall()[3]
        link = "https://thanhnien.vn/" + new.css(" ::attr(href)").get()
        
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
        
        article = {"title": "", "content": "", "link": ""}
        article["title"] = title
        article["content"] = content
        article["link"] = link
        data.append(article)              
        if len(data) == num_articles:
            break  
    with open("data/thanhnien_most_view", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)          
        # print(title)
        # print(content)
        # print(link)
        # print()

if __name__ == "__main__":
    t0 = time.time()
    crawler(40)
    print("Done in: ", time.time() - t0)  