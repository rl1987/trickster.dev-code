import scrapy

from urllib.parse import urljoin

from books_to_scrape.items import Book

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_categories)

    def parse_categories(self, response):
        for category_link in response.xpath('//div[@class="side_categories"]//a'):
            category_url = urljoin(response.url, category_link.attrib.get('href'))
            yield scrapy.Request(category_url, callback=self.parse_book_list)

    def parse_book_list(self, response):
        for book_link in response.xpath('//article[@class="product_pod"]/h3/a'):
            book_url = urljoin(response.url, book_link.attrib.get('href'))
            yield scrapy.Request(book_url, callback=self.parse_book_page)

        next_page_link = response.xpath('//li[@class="next"]/a')
        if next_page_link is not None:
            next_page_url = urljoin(response.url, next_page_link.attrib.get('href'))
            yield scrapy.Request(next_page_url, callback=self.parse_book_list)

    def parse_book_page(self, response):
        item = Book()
        
        item['title'] = response.xpath('//h1/text()').get()
        item['upc'] = response.xpath('//tr[./th[contains(text(), "UPC")]]/td/text()').get()
        item['description'] = response.xpath('//article[@class="product_page"]/p/text()').get()
        item['price_excl_tax'] = response.xpath('//tr[./th[contains(text(), "Price (excl. tax)")]]/td/text()').get()
        item['price_incl_tax'] = response.xpath('//tr[./th[contains(text(), "Price (incl. tax)")]]/td/text()').get()
        item['availability'] = response.xpath('//tr[./th[contains(text(), "Availability")]]/td/text()').get()
        item['n_reviews'] = response.xpath('//tr[./th[contains(text(), "Number of reviews")]]/td/text()').get()

        yield item
