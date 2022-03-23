# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BooksToScrapePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        adapter['price_excl_tax'] = adapter['price_excl_tax'].replace('£', '')
        adapter['price_incl_tax'] = adapter['price_incl_tax'].replace('£', '')
        adapter['availability'] = adapter['availability'].replace('In stock (', '').replace(' available)', '')

        return item
