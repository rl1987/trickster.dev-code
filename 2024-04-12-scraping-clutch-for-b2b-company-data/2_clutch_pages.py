#!/usr/bin/python3

import csv
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pprint import pprint
from urllib.parse import unquote
import time
import threading

from lxml import html

from tls_session import create_session, safe_get

sessions = dict()

def prepare_thread_session():
    sessions[threading.current_thread()] = create_session("https://clutch.co")

def cleanup_phone_no(phone_no):
    phone_no = phone_no.replace("tel:", "")
    phone_no = unquote(phone_no)

    return phone_no

def scrape_company_page(company_url):
    session = sessions[threading.current_thread()]
    resp = safe_get(session, company_url)
    if resp is None or resp.status_code == 403:
        print("Retrying: {}".format(company_url))
        prepare_thread_session()
        session = sessions[threading.current_thread()]
        resp = safe_get(session, company_url)

    if resp is None:
        return None

    print(resp.url, resp.status_code)

    if resp.status_code != 200:
        return None

    tree = html.fromstring(resp.text)

    company_name = tree.xpath("//h1/a/text()")
    if len(company_name) == 1:
        company_name = company_name[0].strip()
    else:
        company_name = None

    company_website = tree.xpath("//h1/a/@href")
    if len(company_website) == 1:
        company_website = company_website[0]
    else:
        company_website = None

    desc_paragraphs = tree.xpath('//div[@itemprop="description"]/p/text()')
    if len(desc_paragraphs) > 0:
        description = " ".join(desc_paragraphs)
        description = description.replace("\n", " ").strip()
    else:
        description = None

    phones = tree.xpath('//a[@itemprop="telephone"]/@href')
    if len(phones) > 0:
        phones = list(map(cleanup_phone_no, phones))
    else:
        phones = []

    min_project = tree.xpath(
        '//li[@data-tooltip-content="<i>Min. project size</i>"]/span[last()]/text()'
    )
    if len(min_project) == 1:
        min_project = min_project[0]
    else:
        min_project = None

    common_project = tree.xpath(
        '//dl[./dt[text()="Most Common Project Size"]]//span/text()'
    )
    if len(common_project) == 1:
        common_project = common_project[0]
        common_project = common_project.strip()
    else:
        common_project = None

    avg_hourly_rate = tree.xpath(
        '//li[@data-tooltip-content="<i>Avg. hourly rate</i>"]/span[last()]/text()'
    )
    if len(avg_hourly_rate) == 1:
        avg_hourly_rate = avg_hourly_rate[0]
    else:
        avg_hourly_rate = None

    n_empl = tree.xpath(
        '//li[@data-tooltip-content="<i>Employees</i>"]/span[last()]/text()'
    )
    if len(n_empl) == 1:
        n_empl = n_empl[0]
    else:
        n_empl = None

    founded = tree.xpath(
        '//li[@data-tooltip-content="<i>Founded</i>"]/span[last()]/text()'
    )
    if len(founded) == 1:
        founded = founded[0]
        founded = founded.replace("Founded ", "")
    else:
        founded = None

    worst_rating = tree.xpath('//meta[@itemprop="worstRating"]/@content')
    if len(worst_rating) == 1:
        worst_rating = worst_rating[0]
    else:
        worst_rating = None

    avg_rating = tree.xpath('//span[@itemprop="ratingValue"]/text()')
    if len(avg_rating) == 1:
        avg_rating = avg_rating[0]
    else:
        avg_rating = None

    best_rating = tree.xpath('//meta[@itemprop="bestRating"]/@content')
    if len(best_rating) == 1:
        best_rating = best_rating[0]
    else:
        best_rating = None

    review_count = tree.xpath('//meta[@itemprop="reviewCount"]/@content')
    if len(review_count) == 1:
        review_count = review_count[0]
    else:
        review_count = None

    street_address = tree.xpath(
        '//meta[@property="business:contact_data:street_address"]/@content'
    )
    if len(street_address) == 1:
        street_address = street_address[0]
    else:
        street_address = None

    locality = tree.xpath('//meta[@property="business:contact_data:locality"]/@content')
    if len(locality) == 1:
        locality = locality[0]
    else:
        locality = None

    region = tree.xpath('//meta[@property="business:contact_data:region"]/@content')
    if len(region) == 1:
        region = region[0]
    else:
        region = None

    postal_code = tree.xpath('//span[@itemprop="postalCode"]/text()')
    if len(postal_code) > 0:
        postal_code = postal_code[0]
    else:
        postal_code = None

    country_name = tree.xpath(
        '//meta[@property="business:contact_data:country_name"]/@content'
    )
    if len(country_name) == 1:
        country_name = country_name[0]
    else:
        country_name = None

    li_url = tree.xpath('//a[@data-type="linkedin"]/@href')
    if len(li_url) > 0:
        li_url = li_url[0]
    else:
        li_url = None

    fb_url = tree.xpath('//a[@data-type="facebook"]/@href')
    if len(fb_url) > 0:
        fb_url = fb_url[0]
    else:
        fb_url = None

    x_url = tree.xpath('//a[@data-type="twitter"]/@href')
    if len(x_url) > 0:
        x_url = x_url[0]
    else:
        x_url = None

    ig_url = tree.xpath('//a[@data-type="instagram"]/@href')
    if len(ig_url) > 0:
        ig_url = ig_url[0]
    else:
        ig_url = None

    row = {
        "company_name": company_name,
        "company_website": company_website,
        "description": description,
        "phones": ", ".join(phones),
        "min_project": min_project,
        "common_project": common_project,
        "avg_hourly_rate": avg_hourly_rate,
        "n_empl": n_empl,
        "worst_rating": worst_rating,
        "avg_rating": avg_rating,
        "best_rating": best_rating,
        "review_count": review_count,
        "street_address": street_address,
        "locality": locality,
        "region": region,
        "postal_code": postal_code,
        "country_name": country_name,
        "li_url": li_url,
        "fb_url": fb_url,
        "ig_url": ig_url,
        "url": company_url,
        "scraped_at": datetime.now().isoformat(),
    }

    return row

FIELDNAMES = [
    "company_name",
    "company_website",
    "description",
    "phones",
    "min_project",
    "common_project",
    "avg_hourly_rate",
    "n_empl",
    "worst_rating",
    "avg_rating",
    "best_rating",
    "review_count",
    "street_address",
    "locality",
    "region",
    "postal_code",
    "country_name",
    "li_url",
    "fb_url",
    "ig_url",
    "url",
    "scraped_at"
]


def main():
    company_urls = []

    in_f = open("lists.csv", "r")
    
    csv_reader = csv.DictReader(in_f)

    for row in csv_reader:
        company_urls.append(row['company_url'])

    in_f.close()
    
    out_f = open("pages.csv", "w+", encoding="utf-8")
    
    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator='\n')
    csv_writer.writeheader()

    with ThreadPoolExecutor(16, initializer=prepare_thread_session) as executor:
        for row in executor.map(scrape_company_page, company_urls):
            if row is None:
                continue
            pprint(row)
            csv_writer.writerow(row)

    out_f.close()

if __name__ == "__main__":
    main()

