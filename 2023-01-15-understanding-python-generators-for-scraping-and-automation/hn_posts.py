#!/usr/bin/python3

import csv
from urllib.parse import urljoin
from pprint import pprint

import requests
from lxml import html

FIELDNAMES = ["title", "url", "points", "discussion_url"]


def scrape_page(i):
    url = "https://news.ycombinator.com/"
    params = {"p": i}

    resp = requests.get(url, params=params)
    print(resp.url)

    tree = html.fromstring(resp.text)

    for athing_row in tree.xpath('//tr[@class="athing"]'):
        title = athing_row.xpath('.//span[@class="titleline"]/a/text()')[0]
        url = athing_row.xpath('.//span[@class="titleline"]/a/@href')[0]
        points = athing_row.xpath(
            './following-sibling::tr//span[@class="score"]/text()'
        )[0].replace(" points", "")
        discussion_url = athing_row.xpath(
            './following-sibling::tr//span[@class="age"]/a/@href'
        )[0]
        discussion_url = urljoin(resp.url, discussion_url)

        yield {
            "title": title,
            "url": url,
            "points": points,
            "discussion_url": discussion_url,
        }


def scrape(n_pages):
    for i in range(1, n_pages + 1):
        yield from scrape_page(i)


def main():
    out_f = open("hn_posts.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for row in scrape(3):
        pprint(row)
        csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()
