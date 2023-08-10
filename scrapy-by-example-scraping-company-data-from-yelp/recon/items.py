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


class CityDataItem(scrapy.Item):
    city = scrapy.Field()
    state = scrapy.Field()
    zip_codes = scrapy.Field()
    murders = scrapy.Field()
    murders_per_cap = scrapy.Field()
    rapes = scrapy.Field()
    rapes_per_cap = scrapy.Field()
    robberies = scrapy.Field()
    robberies_per_cap = scrapy.Field()
    assaults = scrapy.Field()
    assaults_per_cap = scrapy.Field()
    burglaries = scrapy.Field()
    burglaries_per_cap = scrapy.Field()
    thefts = scrapy.Field()
    thefts_per_cap = scrapy.Field()
    auto_thefts = scrapy.Field()
    auto_thefts_per_cap = scrapy.Field()
    arson = scrapy.Field()
    arson_per_cap = scrapy.Field()
    city_data_url = scrapy.Field()
