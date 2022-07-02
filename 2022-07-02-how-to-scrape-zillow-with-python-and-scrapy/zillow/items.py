# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Property(scrapy.Item):
    url = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zipcode = scrapy.Field()
    price = scrapy.Field()
    zestimate = scrapy.Field()
    n_bedrooms = scrapy.Field()
    n_bathrooms = scrapy.Field()
    area = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    phone = scrapy.Field()

    # See: https://docs.scrapy.org/en/latest/topics/media-pipeline.html
    image_urls = scrapy.Field()
    images = scrapy.Field()

