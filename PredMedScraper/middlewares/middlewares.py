# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import datetime

from scrapy.exceptions import IgnoreRequest
from sqlitedict import SqliteDict

class PredmedscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.urls_dict = SqliteDict('./scraped_urls.sqlite', autocommit=True)
        self.urls_dict.load()

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        url_timestamp = self.urls_dict[request]
        if url_timestamp is None:
            self.urls_dict[request] = datetime.datetime.now()
            return None
        else:
            print(request.url + ' already scraped in ' + url_timestamp)
            return IgnoreRequest()
