import scrapy

from scrapy.http import FormRequest

MIN_PRICE = "1000000"
MAX_PRICE = "2000000"

class ClaytonSpider(scrapy.Spider):
    name = 'clayton'
    allowed_domains = ['publicaccess.claytoncountyga.gov']
    start_urls = ['https://publicaccess.claytoncountyga.gov/Search/Disclaimer.aspx?FromUrl=../search/advancedsearch.aspx?mode=advanced']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_cookie_wall)

    def extract_hidden_form_data(self, response):
        form_data = dict()

        for hidden_input in response.xpath('//input[@type="hidden"]'):
            key = hidden_input.attrib.get("id")
            value = hidden_input.attrib.get("value")

            if value is None:
                value = ""

            form_data[key] = value

        return form_data    

    def parse_cookie_wall(self, response):
        form_data = self.extract_hidden_form_data(response)

        form_data['btAgree'] = ""

        self.logger.debug(form_data)
        yield FormRequest(url=response.url, formdata=form_data, callback=self.parse_search_form_page)

    def parse_search_form_page(self, response):
        form_data = self.extract_hidden_form_data(response)
            
        form_data["hdCriteria"] = "price|{}~{}".format(MIN_PRICE, MAX_PRICE)
        form_data["txtCrit"] = MIN_PRICE
        form_data["txtCrit2"] = MAX_PRICE
        form_data["sCriteria"] = "9"
        form_data["hdSelectAllChecked"] = "false"
        form_data["selSortBy"] = "PARID"
        form_data["selSortDir"] = "asc"

        self.logger.debug(form_data)
        yield FormRequest(url=response.url, formdata=form_data, callback=self.parse_search_results)

    def parse_search_results(self, response):
        form_data = self.extract_hidden_form_data(response)
            
        del form_data["rptname"]
        del form_data["pins"]

        rows = response.xpath('//tr[@class="SearchResults"]')

        if len(rows) == 0:
            return

        for tr in rows:
            form_data_details = dict(form_data)
            
            onclick = tr.attrib.get("onclick")
            self.logger.debug("onclick: " + onclick)

            rel_url = onclick.replace("javascript:selectSearchRow('", "").replace("')", "")

            form_data_details['hdLink'] = rel_url
            form_data_details['hdAction'] = 'Link'
    
            self.logger.debug(form_data_details)
            yield FormRequest(url=response.url, formdata=form_data_details, callback=self.parse_details)

        next_page_link = response.xpath('//a[./font/b[text() = "Next >>"]]')
        if next_page_link is not None and form_data.get("PageNum") is not None:
            form_data_next_page = dict(form_data)

            onclick = next_page_link.attrib.get('onclick')
            self.logger.debug("onclick: " + onclick)

            pg_num = onclick.replace("GoToPage(", "").replace(")", "")
            form_data_next_page["PageNum"] = pg_num  #str(int(form_data_next_page["PageNum"]) + 1)
            form_data_next_page["PageSize"] = '15'
            form_data_next_page['hdIndex'] = '0'
            form_data_next_page['hdAction'] = 'NewPage'
    
            self.logger.debug(form_data_next_page)
            yield FormRequest(url=response.url, formdata=form_data_next_page, callback=self.parse_search_results)
        
    def parse_details(self, response):
        property_id = response.xpath('//td[@class="DataletHeaderTop" and contains(text(), "PARID")]/text()').get().strip().replace("PARID: ", "")
        owner = response.xpath('//td[@class="DataletHeaderBottom" and @align="left"]/text()').get()
        address = response.xpath('//td[@class="DataletHeaderBottom" and @align="right"]/text()').get()

        tax_rows = response.xpath('//table[@id="Tax (Penalties and Interest Included through Current Date)"]//tr')

        self.logger.debug(tax_rows)
        
        for tax_row in tax_rows:
            tax_year = tax_row.xpath('./td[1]/text()').get()
            if tax_year == "Year" or tax_year is None:
                continue

            tax_billed = tax_row.xpath('./td[2]/text()').get()
            tax_paid = tax_row.xpath('./td[3]/text()').get()
            tax_due = tax_row.xpath('./td[4]/text()').get()

            item = {
                'property_id': property_id,
                'owner': owner,
                'address': address,
                'tax_year': tax_year,
                'tax_billed': tax_billed,
                'tax_paid': tax_paid,
                'tax_due': tax_due
            }

            yield item

