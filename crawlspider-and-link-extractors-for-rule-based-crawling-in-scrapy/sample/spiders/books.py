import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(allow='index.html', 
                           deny=[
                               'catalogue/page', 
                               'catalogue/category/books', 
                               'https://books.toscrape.com/index.html']
                           ), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow='catalogue/page'), follow=True)
    )


    def parse_item(self, response):
        item = {}

        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('//div[contains(@class, "product_main")]/p[@class="price_color"]/text()').get()
        item['url'] = response.url
        
        return item
