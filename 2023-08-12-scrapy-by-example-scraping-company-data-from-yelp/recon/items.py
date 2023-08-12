# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    # define the fields for your item here like:
    yelp_biz_id = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    phone_number = scrapy.Field()
    website = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    gmaps_img_url = scrapy.Field()
    yelp_url = scrapy.Field()

