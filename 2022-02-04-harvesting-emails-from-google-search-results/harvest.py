#!/usr/bin/python3

import csv
from pprint import pprint
import re
import time
import os

import requests
from lxml import html

FIELDNAMES = ["result_url", "title", "text", "email"]

def scrape_result_page(query, start, num):
    url = "https://www.google.com/search"

    params = {
        "q": query,
        "start": start,
        "num": num,
    }

    while True:
        resp = requests.get(url, params=params, verify=False)
        print(resp.url)

        if resp.status_code == 200:
            break

        time.sleep(1)
        continue

    tree = html.fromstring(resp.text)

    rows = []

    result_divs = tree.xpath('//div[@class="jtfYYd"]')

    for result_div in result_divs:
        result_url = result_div.xpath(".//a/@href")
        if len(result_url) >= 1:
            result_url = result_url[0]
        else:
            result_url = ""

        title = result_div.xpath(".//h3/text()")
        if len(title) == 1:
            title = title[0]
        else:
            title = ""

        snippet_div = result_div.xpath('.//div[@style="-webkit-line-clamp:2"]')
        if len(snippet_div) == 1:
            snippet = snippet_div[0].text_content()
        else:
            snippet = ""

        row = {
            "result_url": result_url,
            "title": title,
            "text": snippet,
        }

        # https://stackoverflow.com/questions/17681670/extract-email-sub-strings-from-large-document
        m = re.search(
            r"(?:\.?)([\w\-_+#~!$&\'\.]+(?<!\.)(@|[ ]?\(?[ ]?(at|AT)[ ]?\)?[ ]?)(?<!\.)[\w]+[\w\-\.]*\.[a-zA-Z-]{2,3})(?:[^\w])",
            snippet + " " + title,
        )

        if m is not None:
            row["email"] = m.groups()[0]
        else:
            continue

        rows.append(row)

    return rows, len(result_divs) < num


def scrape_results(query):
    start = 0
    num = 100

    while True:
        rows, done = scrape_result_page(query, start, num)

        for row in rows:
            yield row

        if done:
            break

        start += num


def main():
    in_f = open("sites.txt", "r")
    sites = in_f.read().strip().split("\n")
    in_f.close()

    in_f = open("q1.txt", "r")
    queries1 = in_f.read().strip().split("\n")
    in_f.close()

    in_f = open("q2.txt", "r")
    queries2 = in_f.read().strip().split("\n")
    in_f.close()

    in_f = open("q3.txt", "r")
    queries3 = in_f.read().strip().split("\n")
    in_f.close()

    out_f = open("emails.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for site in sites:
        for q1 in queries1:
            for q2 in queries2:
                for q3 in queries3:
                    query = 'site:{} "{}" AND "{}" AND "{}"'.format(site, q1, q2, q3)

                    for row in scrape_results(query):
                        pprint(row)
                        csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()

