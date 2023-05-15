# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NikeProductItem(scrapy.Item):
    title = scrapy.Field()
    subtitle = scrapy.Field()
    pid = scrapy.Field()
    current_price = scrapy.Field()
    empl_price = scrapy.Field()
    full_price = scrapy.Field()
    in_stock = scrapy.Field()
    product_url = scrapy.Field()
    image_urls = scrapy.Field()
    description = scrapy.Field()


