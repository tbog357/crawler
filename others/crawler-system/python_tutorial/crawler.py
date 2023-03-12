# Tutorial for multithreading
import threading
import requests
import json

from typing import List


# Local import
from data_model.crawler_job import CrawlerJob
from data_model.crawler_result import CrawlerResult


class CrawlerThread(threading.Thread):
    def __init__(self, crawler_thread_id):
        threading.Thread.__init__(self)
        self.crawler_thread_id = crawler_thread_id
        self.crawler_job = None
        self.crawler_result = None

    def set_crawler_job(self, crawler_job: CrawlerJob):
        self.crawler_job = crawler_job

    def unset_crawler_job(self):
        self.crawler_job = None

    def run(self):
        if self.crawler_job is None:
            return

        # Logging
        print(
            {
                "crawler_thread_id": self.crawler_thread_id,
                "crawler_job": self.crawler_job.__dict__,
            }
        )

        # Crawl the data
        resp = requests.get(self.crawler_job.url)

        # Build the result model
        self.crawler_result = CrawlerResult(
            crawler_thread_id=self.crawler_thread_id,
            crawler_job=self.crawler_job,
            resp=resp.text,
        )
        # Remove the job
        self.unset_crawler_job()

        # Save the data
        self.save_crawler_result()

    def save_crawler_result(self):
        json.dump(self.crawler_result.to_dict(), open(f"output/{self.crawler_thread_id}.json", "w"))


if __name__ == "__main__":
    # Read from database
    urls = json.load(open("input.json", "r"))

    crawler_threads: List[threading.Thread] = []
    for idx, url in enumerate(urls):
        # Create crawler thread
        thread = CrawlerThread(str(idx))

        # Crate job from schema
        crawler_job = CrawlerJob(url)

        # Set job for thread
        thread.set_crawler_job(crawler_job)

        # Store thread reference
        crawler_threads.append(thread)

    # Start threads
    for thread in crawler_threads:
        thread.start()

    # Wait group
    for thread in crawler_threads:
        thread.join()
