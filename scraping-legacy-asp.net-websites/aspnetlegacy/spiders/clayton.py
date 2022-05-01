import scrapy

from scrapy.http import FormRequest

class ClaytonSpider(scrapy.Spider):
    name = 'clayton'
    allowed_domains = ['publicaccess.claytoncountyga.gov']
    start_urls = ['https://publicaccess.claytoncountyga.gov/Search/Disclaimer.aspx?FromUrl=../search/advancedsearch.aspx?mode=advanced']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_cookie_wall)

    def parse_cookie_wall(self, response):
        form_data = dict()

        for hidden_input in response.xpath("//input"):
            key = hidden_input.attrib.get("id")
            value = hidden_input.attrib.get("value")

            if value is None:
                value = ""

            form_data[key] = value

        form_data['btAgree'] = ""

        yield FormRequest(url=response.url, formdata=form_data, callback=self.parse_search_form_page)

    def parse_search_form_page(self, response):
        pass

