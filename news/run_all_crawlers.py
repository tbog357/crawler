from threading import Thread
from news_crawler.spiders.base import BaseCrawler
from news_crawler.spiders.laodong import LaodongCrawler
from news_crawler.spiders.nhandan import NhandanCrawler
from news_crawler.spiders.dantri import DantriCrawler
from news_crawler.spiders.vnexpress import Vnexpress1Crawler, Vnexpress2Crawler

if __name__ == "__main__":
    new_crawler_list: list[BaseCrawler] = [
        NhandanCrawler,
        DantriCrawler,
        LaodongCrawler,
        Vnexpress1Crawler,
        Vnexpress2Crawler,
    ]

    all_threads = []

    for crawler in new_crawler_list:
        for cate in crawler.cate_list:
            thread: Thread = crawler(cate, crawler.gen_link(cate), 10)
            thread.start()

            all_threads.append(thread)

    for thread in all_threads:
        thread.join()
