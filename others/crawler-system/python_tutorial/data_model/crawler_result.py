from base_data_model import BaseDataModel
from crawler_job import CrawlerJob

class CrawlerResult(BaseDataModel):
    def __init__(self, crawler_thread_id: str, crawler_job: CrawlerJob, resp: str):
        self.crawler_thread_id = crawler_thread_id
        self.crawler_job = crawler_job
        self.resp = resp

    def to_dict(self):
        self.crawler_job = self.crawler_job.__dict__
        return self.__dict__
