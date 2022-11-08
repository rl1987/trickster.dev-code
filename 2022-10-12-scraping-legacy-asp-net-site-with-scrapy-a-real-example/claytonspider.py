import scrapy

from scrapy.http import FormRequest
from dateutil.parser import parse as parse_datetime

import calendar
from datetime import datetime, date
import logging
from urllib.parse import urljoin

from housingprices.items import SalesItem


class ClaytonSpider(scrapy.Spider):
    name = "clayton"
    allowed_domains = ["publicaccess.claytoncountyga.gov"]
    start_urls = [
        "https://publicaccess.claytoncountyga.gov/Search/Disclaimer.aspx?FromUrl=../search/advancedsearch.aspx?mode=advanced",
        "https://publicaccess.claytoncountyga.gov/search/advancedsearch.aspx?mode=advanced",
    ]
    start_year = 1939
    state = "GA"
    county = "CLAYTON"
    shards = []
    stats_filepath = None

    def __init__(self, year=None, month=None, stats_filepath=None):
        super().__init__()

        self.stats_filepath = stats_filepath

        if year is not None and month is not None:
            year = int(year)
            month = int(month)
            self.shards = [(year, month)]
            return

        for year in range(self.start_year, datetime.today().year + 1):
            for month in range(1, 13):
                shard = (year, month)
                self.shards.append(shard)

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_disclaimer_page)

    def parse_disclaimer_page(self, response):
        yield FormRequest.from_response(
            response,
            formxpath='//form[@name="Form1"]',
            clickdata={"name": "btAgree"},
            callback=self.parse_form_page,
        )

    def stringify_date(self, d):
        return "{:02d}/{:02d}/{:04d}".format(d.month, d.day, d.year)

    def extract_form(self, response, form_xpath):
        form_data = dict()

        for hidden_input in response.xpath(form_xpath).xpath(".//input"):
            name = hidden_input.attrib.get("name")
            if name is None:
                continue
            value = hidden_input.attrib.get("value")
            if value is None:
                value = ""

            form_data[name] = value

        return form_data

    def make_search_form_request(self, response, start_date, end_date):
        start_date_str = self.stringify_date(start_date)
        end_date_str = self.stringify_date(end_date)

        form_data = self.extract_form(response, '//form[@name="frmMain"]')

        form_data["hdCriteria"] = "salesdate|{}~{}".format(start_date_str, end_date_str)
        form_data["ctl01$cal1"] = start_date.isoformat()
        form_data["ctl01$cal1$dateInput"] = start_date_str
        form_data["txtCrit"] = start_date_str
        form_data["ctl01$cal2"] = end_date.isoformat()
        form_data["ctl01$cal2$dateInput"] = end_date_str
        form_data["txtCrit2"] = end_date_str
        form_data["PageNum"] = "1"
        form_data["PageSize"] = "1"
        form_data["hdCriteriaTypes"] = "N|N|C|C|C|N|C|C|N|D|N|N|C|C|C|N|N"
        form_data["sCriteria"] = "0"

        logging.debug(form_data)

        return FormRequest(
            response.url,
            formdata=form_data,
            callback=self.parse_search_result_list,
            dont_filter=True,
        )

    def parse_form_page(self, response):
        if len(self.shards) == 0:
            yield None
            return

        year, month = self.shards.pop()
        logging.info("Year: {}, month: {}".format(year, month))

        days_in_month = calendar.monthrange(year, month)[1]

        start_date = date(year=year, month=month, day=1)
        end_date = date(year=year, month=month, day=days_in_month)

        yield self.make_search_form_request(response, start_date, end_date)

    def parse_search_result_list(self, response):
        first_row = response.xpath('//tr[@class="SearchResults"][1]')
        if len(first_row) != 1:
            yield scrapy.Request(
                self.start_urls[-1], callback=self.parse_form_page, dont_filter=True
            )
            return

        logging.debug(first_row.xpath(".//text()").getall())

        onclick = first_row.attrib.get("onclick")
        rel_url = onclick.replace("javascript:selectSearchRow('", "").replace("')", "")

        form_data = self.extract_form(response, '//form[@name="frmMain"]')
        form_data["hdLink"] = rel_url
        form_data["hdAction"] = "Link"
        form_data["hdSelectAllChecked"] = "false"
        form_data["sCriteria"] = "0"
        logging.debug(form_data)

        action = response.xpath('//form[@name="frmMain"]/@action').get()
        form_url = urljoin(response.url, action)

        yield FormRequest(
            form_url,
            formdata=form_data,
            callback=self.parse_property_main_page,
            dont_filter=True,
        )

    def parse_property_main_page(self, response):
        parid = response.xpath('//input[@id="hdXPin"]/@value').get()
        property_street_address = (
            response.xpath('//td[@class="DataletHeaderBottom"][last()]/text()')
            .get("")
            .strip()
        )
        property_street_address = " ".join(
            property_street_address.split()
        )  # https://stackoverflow.com/a/1546251

        item = SalesItem()
        item["state"] = self.state
        item["property_id"] = parid
        item["property_street_address"] = property_street_address
        item["property_county"] = self.county
        item["property_type"] = response.xpath(
            '//tr[./td[contains(text(),"Property Class")]]/td[@class="DataletData"]/text()'
        ).get()

        residential_link = response.xpath(
            '//a[./span[text()="Residential"]]/@href'
        ).get()
        yield response.follow(
            residential_link,
            meta={"item": item},
            callback=self.parse_property_residential_page,
            dont_filter=True,
        )

    def parse_property_residential_page(self, response):
        item = response.meta.get("item")

        parid = response.xpath('//input[@id="hdXPin"]/@value').get()
        assert parid == item["property_id"]

        item["building_year_built"] = response.xpath(
            '//tr[./td[text()="Year Built"]]/td[@class="DataletData"]/text()'
        ).get()
        item["building_num_beds"] = response.xpath(
            '//tr[./td[text()="Bedrooms"]]/td[@class="DataletData"]/text()'
        ).get()
        item["building_num_baths"] = response.xpath(
            '//tr[./td[text()="Full Baths"]]/td[@class="DataletData"]/text()'
        ).get()

        value_history_link = response.xpath(
            '//a[./span[text()="Value History"]]/@href'
        ).get()
        yield response.follow(
            value_history_link,
            meta={"item": item},
            callback=self.parse_property_value_history_page,
            dont_filter=True,
        )

    def parse_property_value_history_page(self, response):
        item = response.meta.get("item")
        appr_rows = response.meta.get("appr_rows")
        as_rows = response.meta.get("as_rows")

        appr_rows = dict()
        appr_header = None

        appr_values_table = response.xpath('//table[@id="Appraised Values"]')
        if appr_values_table is not None:
            for row in appr_values_table.xpath("./tr"):
                row = row.xpath("./td/text()").getall()
                if appr_header is None:
                    appr_header = row
                    continue

                if len(row) == 0:
                    continue

                year = row[0]
                try:
                    year = int(year)
                except:
                    continue
                row = dict(zip(appr_header, row))
                appr_rows[year] = row

        logging.debug(appr_rows)

        as_rows = dict()
        as_header = None

        as_values_table = response.xpath('//table[@id="Assessed Values"]')
        if as_values_table is not None:
            for row in as_values_table.xpath("./tr"):
                row = row.xpath("./td/text()").getall()
                if as_header is None:
                    as_header = row
                    continue

                if len(row) == 0:
                    continue

                year = row[0]
                try:
                    year = int(year)
                except:
                    continue
                row = dict(zip(as_header, row))
                as_rows[year] = row

        logging.debug(as_rows)

        meta_dict = {"item": item, "appr_rows": appr_rows, "as_rows": as_rows}

        land_link = response.xpath('//a[./span[text()="Land"]]/@href').get()
        yield response.follow(
            land_link,
            meta=meta_dict,
            callback=self.parse_property_land_page,
            dont_filter=True,
        )

    def parse_property_land_page(self, response):
        item = response.meta.get("item")
        appr_rows = response.meta.get("appr_rows")
        as_rows = response.meta.get("as_rows")

        item["land_area_acres"] = (
            response.xpath('//tr[./td[text()="Acres"]]/td[@class="DataletData"]/text()')
            .get("")
            .replace("\xa0", "")
        )
        if item["land_area_acres"].startswith("."):
            item["land_area_acres"] = 0
        elif item["land_area_acres"] != "":
            item["land_area_acres"] = round(float(item["land_area_acres"]))
        item["land_area_sqft"] = (
            response.xpath(
                '//tr[./td[text()="Square Feet"]]/td[@class="DataletData"]/text()'
            )
            .get("")
            .replace("\xa0", "")
            .replace(",", "")
        )
        item["land_type"] = response.xpath(
            '//tr[./td[text()="Land Type"]]/td[@class="DataletData"]/text()'
        ).get()

        meta_dict = {"item": item, "appr_rows": appr_rows, "as_rows": as_rows}

        sales_link = response.xpath('//a[./span[text()="Sales"]]/@href').get()
        yield response.follow(
            sales_link,
            meta=meta_dict,
            callback=self.parse_property_sales_page,
            dont_filter=True,
        )

    def parse_property_sales_page(self, response):
        item = response.meta.get("item")
        appr_rows = response.meta.get("appr_rows")
        as_rows = response.meta.get("as_rows")

        sale_date_str = response.xpath(
            '//tr[./td[text()="Sale Date"]]/td[@class="DataletData"]/text()'
        ).get()
        if sale_date_str is not None:
            sale_date_str = parse_datetime(sale_date_str).isoformat().replace("T", " ")

        item["sale_datetime"] = sale_date_str
        item["sale_price"] = (
            response.xpath(
                '//tr[./td[text()="Sale Price"]]/td[@class="DataletData"]/text()'
            )
            .get("")
            .replace("$", "")
            .replace(",", "")
        )
        item["seller_1_name"] = (
            response.xpath(
                '//tr[./td[text()="Grantor"]]/td[@class="DataletData"]/text()'
            )
            .get("")
            .replace("\xa0", "")
        )
        item["buyer_1_name"] = (
            response.xpath(
                '//tr[./td[text()="Grantee"]]/td[@class="DataletData"]/text()'
            )
            .get("")
            .replace("\xa0", "")
        )
        item["seller_2_name"] = (
            response.xpath(
                '//tr[./td[text()="Grantor 2"]]/td[@class="DataletData"]/text()'
            )
            .get("")
            .replace("\xa0", "")
        )
        item["buyer_2_name"] = (
            response.xpath(
                '//tr[./td[text()="Grantee 2"]]/td[@class="DataletData"]/text()'
            )
            .get("")
            .replace("\xa0", "")
        )
        item["book"] = response.xpath(
            '//tr[./td[text()="Deed Book"]]/td[@class="DataletData"]/text()'
        ).get()
        item["page"] = response.xpath(
            '//tr[./td[text()="Deed Page"]]/td[@class="DataletData"]/text()'
        ).get()
        item["transfer_deed_type"] = response.xpath(
            '//tr[./td[text()="Instrument Type"]]/td[@class="DataletData"]/text()'
        ).get()
        item[
            "source_url"
        ] = "https://publicaccess.claytoncountyga.gov/search/advancedsearch.aspx?mode=advanced"

        appr_row = appr_rows.get(sale_date.year)
        if appr_row is not None:
            item["total_appraised_value"] = appr_row.get("Total", "").replace(",", "")
            item["land_appraised_value"] = appr_row.get("Land", "").replace(",", "")
            item["building_appraised_value"] = appr_row.get("Building", "").replace(
                ",", ""
            )
        else:
            item["total_appraised_value"] = None
            item["land_appraised_value"] = None
            item["building_appraised_value"] = None

        as_row = as_rows.get(sale_date.year)
        if as_row is not None:
            item["building_assessed_value"] = as_row.get("Buidling", "").replace(
                ",", ""
            )
            item["building_assessed_date"] = sale_date.year
            item["land_assessed_value"] = as_row.get("Land", "").replace(",", "")
            item["total_assessed_value"] = as_row.get("Total", "").replace(",", "")
        else:
            item["building_assessed_value"] = None
            item["building_assessed_value"] = None
            item["land_assessed_value"] = None
            item["total_assessed_value"] = None

        yield item

        next_sale_link = response.xpath(
            '//a[./i[@class="icon-angle-right "]]/@href'
        ).get()
        if next_sale_link is not None:
            yield response.follow(
                next_sale_link,
                callback=self.parse_property_sales_page,
                dont_filter=True,
                meta={"item": item},
            )
            return

        to_from_input_text = response.xpath(
            '//input[@name="DTLNavigator$txtFromTo"]/@value'
        ).get()
        idx, total = to_from_input_text.split(" of ")
        idx = int(idx)
        total = int(total)

        if idx == total:
            yield scrapy.Request(
                self.start_urls[-1],
                callback=self.parse_form_page,
                dont_filter=True,
                meta={"item": item},
            )
            return

        form_data = self.extract_form(response, '//form[@name="frmMain"]')
        del form_data["DTLNavigator$imageNext"]
        del form_data["DTLNavigator$imageLast"]
        form_data["DTLNavigator$imageNext.x"] = "0"  # XXX
        form_data["DTLNavigator$imageNext.y"] = str(idx + 1)
        form_data["hdMode"] = "DEK_PROFILE"
        logging.info(form_data)

        action = response.xpath('//form[@name="frmMain"]/@action').get()
        form_url = urljoin(response.url, action).replace(
            "mode=sales", "mode=dek_profile"
        )

        yield FormRequest(
            form_url,
            formdata=form_data,
            callback=self.parse_property_main_page,
            dont_filter=True,
        )
