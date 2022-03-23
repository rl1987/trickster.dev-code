# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Book(scrapy.Item):
    title = scrapy.Field()
    upc = scrapy.Field()
    description = scrapy.Field()
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    availability = scrapy.Field()
    n_reviews = scrapy.Field()
