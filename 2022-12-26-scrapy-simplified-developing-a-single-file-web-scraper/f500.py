#!/usr/bin/python3

import json

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

class F500Spider(scrapy.Spider):
    start_urls = ["https://fortune.com/ranking/fortune500/2022/search/"]
    name = "f500"

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_search)

    def parse_search(self, response):
        json_str = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        json_dict = json.loads(json_str)

        item_dicts = (
            json_dict.get("props", dict())
            .get("pageProps", dict())
            .get("franchiseList", dict())
            .get("items", [])
        )

        for item_dict in item_dicts:
            slug = item_dict.get("slug")
            rank = item_dict.get("data", dict()).get("Rank", "").replace(",", "")
            rank = int(rank)

            if slug is not None and rank <= 500:
                yield response.follow(slug, callback=self.parse_company_page)

    # TODO: make it scrape this as well: https://fortune.com/company/amphenol/fortune500/
    def parse_company_page(self, response):
        json_str = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        try:
            json_dict = json.loads(json_str)
        except:
            return
        
        fli = json_dict.get("props", dict()).get("pageProps", dict()).get("franchiseListItem")
        if fli is None:
            return

        company_name = fli.get("title")
        rank = fli.get("rank")

        company_info = fli.get("companyInfo", dict())

        website = company_info.get("Website")
        if website is not None and website.startswith("<a"):
            website = Selector(text=website).xpath('//a/text()').get()
    
        country = company_info.get("Country")
        industry = company_info.get("Industry")
        ticker = company_info.get("Ticker")

        yield {
            "rank": rank,
            "company_name": company_name,
            "website": website,
            "country": country,
            "industry": industry,
            "ticker": ticker
        }


def main():
    # See: https://docs.scrapy.org/en/latest/topics/practices.html#run-from-script
    process = CrawlerProcess(settings={
        "FEEDS": {
            "f500.csv": {"format": "csv"}
        }
    })
    process.crawl(F500Spider)
    process.start()


if __name__ == "__main__":
    main()
