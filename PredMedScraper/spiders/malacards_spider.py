from pathlib import Path
import scrapy
import urllib.parse

class MalaCardsSpider(scrapy.Spider):
    name = "malacards"
    allowed_domains = ['www.malacards.org']
    start_urls = ['https://www.malacards.org/categories']
    file_urls = []

    HDRs = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self):
        urls = [
            "https://www.malacards.org/categories",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
            }
            )

    def encode_url(self, response, node):
        url = node.get()
        if '?' in url:
            relative_url, get_parameters = url.split('?')
            return response.urljoin(urllib.parse.quote(relative_url)) + '?' + urllib.parse.quote(get_parameters)
        return response.urljoin(urllib.parse.quote(node.get()))

    def parse(self, response):
        categories = response.xpath('//a[contains(@href, "categories/")]/@href')
        for category in categories:
            print('Category:', response.urljoin(category.get()))
            yield scrapy.Request(url=response.urljoin(category.get()), callback=self.parse_categories)

    def parse_categories(self, response):
        cards = response.xpath('//a[contains(@href, "/card/") and contains(@href, "?search=")]/@href')
        for card in cards:
            print('Card: ', self.encode_url(response, card))
            yield scrapy.Request(url=self.encode_url(response, card), callback=self.parse_cards)

    def parse_cards(self, response):
        yield {'file_urls': [response.url]}
        #print(response.url)

# from scrapy.crawler import CrawlerProcess
#
# c = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/5.0',
#
#         # save in file CSV, JSON or XML
#         #'FEED_FORMAT': 'csv',     # csv, json, xml
#         #'FEED_URI': 'output.csv', #
#
#         # used standard FilesPipeline (download to FILES_STORE/full)
#     'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},
#
#         # this folder has to exist before downloading
#     'FILES_STORE': '.',
# })
#
# c.crawl(MalaCardsSpider)
# c.start()