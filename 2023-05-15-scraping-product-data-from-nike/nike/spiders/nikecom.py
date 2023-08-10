import scrapy

import json
from urllib.parse import urlencode

from nike.items import NikeProductItem

class NikecomSpider(scrapy.Spider):
    name = 'nikecom'
    allowed_domains = ['nike.com', 'www.nike.com', 'api.nike.com']
    start_urls = ['https://www.nike.com/w/?vst=']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_first_page)

    def convert_product_dict_into_item(self, product):
        item = NikeProductItem()
        
        item['title'] = product.get("title")
        item['subtitle'] = product.get("subtitle")
        item['pid'] = product.get("pid")
        
        price_dict = product.get("price", dict())
        if price_dict is not None:
            item['current_price'] = price_dict.get("currentPrice")
            item['empl_price'] = price_dict.get("employeePrice")
            item['full_price'] = price_dict.get("fullPrice")

        item['in_stock'] = product.get("inStock")
        item['product_url'] = product.get('url')
        if item['product_url'] is not None:
            item['product_url'] = item['product_url'].replace("{countryLang}", "https://www.nike.com")

        return item

    def create_feed_api_request(self, next_page_link):
        params = {
            'queryid': 'products',
            'anonymousId': '7CC266B713D36CCC7275B33B6E4F9206', #XXX
            'country': 'us',
            'endpoint': next_page_link,
            'language': 'en',
            'localizedRangeStr': '{lowestPrice} — {highestPrice}'
        }

        url = 'https://api.nike.com/cic/browse/v2'

        url = url + '?' + urlencode(params)

        return scrapy.Request(url, callback=self.parse_product_feed)

    def parse_first_page(self, response):
        next_data_json_str = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        json_dict = json.loads(next_data_json_str)
        props = json_dict.get("props")
        page_props = props.get("pageProps")
        initial_state = page_props.get("initialState")
        wall = initial_state.get("Wall")
        products = wall.get('products')

        for product in products:
            item = self.convert_product_dict_into_item(product)
            if item.get('product_url') is not None:
                yield scrapy.Request(item['product_url'], meta={'item': item}, callback=self.parse_product_page)

        page_data = wall.get('pageData')
        if page_data is not None:
            next_page_link = page_data.get("next")
            if next_page_link is not None and next_page_link != '':
                yield self.create_feed_api_request(next_page_link)

    def parse_product_page(self, response):
        item = response.meta.get('item')
        
        item['description'] = response.xpath('//div[contains(@class, "description-preview")]/p/text()').get()
        item['image_urls'] = response.xpath('//picture/source/@srcset').getall()

        yield item

    def parse_product_feed(self, response):
        json_str = response.text

        json_dict = json.loads(json_str)

        products = json_dict.get('data', dict()).get('products', dict()).get('products', [])

        for product in products:
            item = self.convert_product_dict_into_item(product)
            yield scrapy.Request(item['product_url'], meta={'item': item}, callback=self.parse_product_page)

        next_page_link = json_dict.get('data', dict()).get('products', dict()).get('pages', dict()).get('next')
        if next_page_link is not None and next_page_link != '':
            yield self.create_feed_api_request(next_page_link)

