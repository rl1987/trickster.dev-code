import scrapy

from urllib.parse import urlencode, urlparse, parse_qsl

from recon.items import YelpItem


class YelpSpider(scrapy.Spider):
    name = "yelp"
    allowed_domains = ["yelp.com"]
    start_urls = ["http://yelp.com/"]

    locations = None
    queries = None

    def __init__(self, locations="United States", queries="Pizza|Coffee"):
        super().__init__()

        self.locations = locations.split("|")
        self.queries = queries.split("|")

    def start_requests(self):
        for location in self.locations:
            for query in self.queries:
                url = "https://www.yelp.com/search"

                params = {"find_desc": query, "find_loc": location}

                url = url + "?" + urlencode(params)

                yield scrapy.Request(
                    url, callback=self.parse_company_list, meta={"category": query}
                )

    def parse_company_list(self, response):
        category = response.meta.get("category")

        company_links = response.xpath(
            '//a[starts-with(@href, "/biz/")]/@href'
        ).getall()
        company_links = list(map(lambda cl: cl.split("?")[0], company_links))
        company_links = list(set(company_links))

        for company_link in company_links:
            yield response.follow(
                company_link,
                callback=self.parse_company_details,
                meta={"category": category},
            )

        next_page_url = response.xpath('//a[@aria-label="Next"]/@href').get()
        if next_page_url is not None:
            yield scrapy.Request(
                next_page_url,
                callback=self.parse_company_list,
                meta={"category": category},
            )

    def parse_company_details(self, response):
        category = response.meta.get("category")

        item = YelpItem()

        item["category"] = category

        item["yelp_biz_id"] = response.xpath(
            '//meta[@name="yelp-biz-id"]/@content'
        ).get()

        item["name"] = response.xpath("//h1/text()").get()

        item["description"] = response.xpath(
            '//meta[@property="og:description"]/@content'
        ).get()
        if item["description"] is not None:
            item["description"] = item["description"].replace("\n", " ").strip()

        item["phone_number"] = response.xpath(
            '//div[./p[text()="Phone number"]]/p[last()]/text()'
        ).get()
        item["website"] = response.xpath(
            '//div[./p[text()="Business website"]]/p[last()]/a/@href'
        ).get()
        if item["website"] is not None and item["website"].startswith("/biz_redir"):
            o = urlparse(item["website"])
            params = parse_qsl(o.query)
            params = dict(params)
            item["website"] = params.get("url")

        item["address"] = response.xpath(
            '//div[./p/a[text()="Get Directions"]]/p[last()]/text()'
        ).get()

        gmaps_img_url = response.xpath(
            '//img[contains(@src, "maps.googleapis.com")]/@src'
        ).get()

        o = urlparse(gmaps_img_url)
        gmaps_params = parse_qsl(o.query)
        gmaps_params = dict(gmaps_params)

        self.logger.debug(gmaps_params)

        center = gmaps_params.get("center")
        if center is None:
            try:
                center = gmaps_params.get("markers").split("|")[-1]
            except:
                pass

        if center is not None:
            latitude, longitude = center.split(",")

            item["latitude"] = latitude
            item["longitude"] = longitude

        item["gmaps_img_url"] = gmaps_img_url
        item["yelp_url"] = response.url

        yield item
