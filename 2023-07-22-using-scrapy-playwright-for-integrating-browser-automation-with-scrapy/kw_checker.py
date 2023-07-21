#!/usr/bin/python3

import argparse
from datetime import datetime
import sys
import os
from urllib.parse import urlparse
import logging

import scrapy
from scrapy.crawler import CrawlerProcess


class KeywordSpider(scrapy.Spider):
    name = "kwchecker"
    start_urls = []
    allowed_domains = []
    keywords = []
    use_playwright = False

    def __init__(self, start_urls, keywords, use_playwright, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = list(set(start_urls))

        allowed_domains = []
        for start_url in self.start_urls:
            domain = urlparse(start_url).netloc
            allowed_domains.append(domain)

        self.allowed_domains = list(set(allowed_domains))
        self.keywords = list(set(keywords))
        self.use_playwright = use_playwright

    def start_requests(self):
        meta = {"playwright": self.use_playwright}
        for start_url in self.start_urls:
            yield scrapy.Request(start_url, meta=meta)

    def parse(self, response):
        meta = dict()
        if response.meta.get("playwright") is not None:
            meta["playwright"] = response.meta.get("playwright")
        try:
            text = " ".join(response.xpath("*//text()").getall()).strip()
        except:
            return

        for keyword in self.keywords:
            if keyword.lower() in text.lower():
                yield {
                    "keyword": keyword,
                    "url": response.url,
                    "seen_at": datetime.now().isoformat(),
                }

        links = response.xpath("//a/@href").getall()
        for link in links:
            o = urlparse(link)
            if o.scheme == "" or o.scheme == "http" or o.scheme == "https":
                yield response.follow(link, meta=meta)


def read_lines(file_path):
    in_f = open(file_path, "r")
    lines = in_f.read().strip().split("\n")
    in_f.close()

    lines = list(map(lambda line: line.strip(), lines))
    lines = list(set(lines))

    return lines


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start-urls",
        required=False,
        help="List of start URLs, one per line",
        default="start_urls.txt",
    )
    parser.add_argument(
        "--keywords",
        required=False,
        help="List of keywords, one per line",
        default="keywords.txt",
    )
    parser.add_argument(
        "--use-playwright",
        required=False,
        help="Use Playwright",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--output-csv-file",
        required=False,
        help="Output CSV file",
        default="output.csv",
    )

    parsed_args = vars(parser.parse_args(sys.argv[1:]))
    print("Parsed CLI args: {}".format(parsed_args))

    start_urls = read_lines(parsed_args.get("start_urls"))
    keywords = read_lines(parsed_args.get("keywords"))
    output_csv_file = parsed_args.get("output_csv_file")
    use_playwright = parsed_args.get("use_playwright")

    if os.path.isfile(output_csv_file):
        os.unlink(output_csv_file)

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }

    settings = {
        "USER_AGENT": headers.get("user-agent"),
        "DEFAULT_REQUEST_HEADERS": headers,
        "FEEDS": {output_csv_file: {"format": "csv"}},
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    }

    if use_playwright:
        settings["DOWNLOAD_HANDLERS"] = {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        }

        settings[
            "TWISTED_REACTOR"
        ] = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

    process = CrawlerProcess(settings=settings)

    process.crawl(KeywordSpider, start_urls, keywords, use_playwright)
    process.start()


if __name__ == "__main__":
    main()
