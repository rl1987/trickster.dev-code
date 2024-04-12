#!/usr/bin/python3

import csv
from urllib.parse import urljoin
import time

from lxml import html

from tls_session import create_session

session = None


def get_category_urls(session):
    resp = session.get("https://clutch.co/sitemap")
    print(resp.url, resp.status_code)

    tree = html.fromstring(resp.text)

    urls = set()

    for link in tree.xpath('//a[@class="sitemap-data__wrap-link"]/@href'):
        urls.add(urljoin(resp.url, link))

    return list(urls)


def get_company_urls(category_url):
    global session

    company_urls = list()

    while True:
        try:
            resp = session.get(category_url)
        except Exception as e:
            print(e)
            time.sleep(1)
            continue

        if resp.status_code == 403:
            time.sleep(1)
            session = create_session(category_url)
            continue

        print(resp.url, resp.status_code)

        tree = html.fromstring(resp.text)

        for company_link in tree.xpath(
            '//h3[@class="company_info"]/a[contains(@href, "/profile")]/@href'
        ):
            company_url = urljoin(resp.url, company_link)
            company_urls.append(company_url)

        next_page_link = tree.xpath('//a[text()="next"]/@href')
        if len(next_page_link) == 0:
            break

        next_page_link = next_page_link[0]
        category_url = urljoin(resp.url, next_page_link)

    return company_urls


def main():
    global session

    session = create_session("https://clutch.co")

    print(session.cookies)

    category_urls = get_category_urls(session)

    out_f = open("lists.csv", "w+", encoding="utf-8")

    csv_writer = csv.DictWriter(
        out_f, fieldnames=["category_url", "company_url"], lineterminator="\n"
    )
    csv_writer.writeheader()

    seen = dict()

    for category_url in category_urls:
        company_urls = get_company_urls(category_url)

        for company_url in company_urls:
            if seen.get(company_url):
                continue
            
            print(category_url, company_url)

            csv_writer.writerow(
                {"category_url": category_url, "company_url": company_url}
            )

            seen[company_url] = True

    out_f.close()


if __name__ == "__main__":
    main()
