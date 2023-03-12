from base_data_model import BaseDataModel

class CrawlerJob(BaseDataModel):
    def __init__(self, url: str):
        self.url = url