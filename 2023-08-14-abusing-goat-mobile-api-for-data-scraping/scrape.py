#!/usr/bin/python3

import csv
import sys
from pprint import pprint
from urllib.parse import quote
import time

import requests

# ISP proxy URL
PROXY_URL = "[REDACTED]"

COUNTRY_CODE = "US"
CURRENCY = "USD"

FIELDNAMES = [
    "template_id",
    "slug",
    "name",
    "img_url",
    "brand",
    "sku",
    "box_condition",
    "shoe_condition",
    "size",
    "stock_status",
    "lowest_price",
]

RETRIES = 5

def create_session():
    session = requests.Session()

    session.headers = {
        "x-px-authorization": "3",
        "accept": "application/json",
        "authorization": 'Token token=""',
        "accept-language": "en-GB,en;q=0.9",
        "x-emb-st": "1691934124434",
        "user-agent": "GOAT/2.62.0 (iPhone; iOS 16.6; Scale/2.00) Locale/en",
        "x-emb-id": "A131256965044D838D97E9AEC3CC32DE",
        "x-px-original-token": "3:7b9f8feffc454bb265869bb69319201a10c0733ded5f64415904867ca6015448:V3kOFKugd0IYEzhYfgTK4QOh8dWCzZH04C4uoGYEfOekVmjMvCYLle7yVImUv8bSOoVChlY3FPELVmFZLboPxA==:1000:V6naWWAGfhIA54bPIFXyWPSpd7e9WmoWghqXoB1xwiAb0TVePEULt5nHoZFhWkpg1E4ZjMtwt1N9yfV2HCYOklHUqUy+oaAlYkACXQLwqsD21d70W55yb0UY9qHQHxY9zQcr6th//3ckUVLU/v1yWhZt/GV9jNyf6EesLG9fw+gqMWPhrpi8bDT1j5eeTR9BLmWMqrY3hmQSYRc9C7K5pQ==",
    }

    session.proxies = {"http": PROXY_URL, "https": PROXY_URL}

    session.cookies.set("currency", CURRENCY)

    return session


def get_product_template_data(session, product_slug):
    url = "https://www.goat.com/api/v1/product_templates/{}/show_v2".format(product_slug)

    resp = session.get(url)
    print(resp.url)

    return resp.json()

def get_buy_bar_data(session, product_slug):
    url = "https://www.goat.com/api/v1/product_variants/buy_bar_data"

    params = {
        'countryCode': COUNTRY_CODE,
        'productTemplateId': product_slug
    }

    tries_left = RETRIES

    while tries_left > 0:
        resp = session.get(url, params=params)
        print(resp.url)

        if resp.status_code == 200:
            break
        
        tries_left -= 1
        time.sleep(1)

    if resp.status_code == 200:
        return resp.json()
    else:
        return None

def scrape_search(session, search_query):
    page = 1

    url = "https://goat.cnstrc.com/search/" + quote(search_query)

    params = {
        "key": "key_XT7bjdbvjgECO5d8",
        "page": str(page),
        "fmt_options[hidden_fields]": "gp_instant_ship_lowest_price_cents_2",
        "fmt_options[hidden_facets]": "gp_instant_ship_lowest_price_cents_2",
        "features[display_variations]": "true",
        "feature_variants[display_variations]": "matched",
        "variations_map": '{"dtype":"object","group_by":[{"name":"product_condition","field":"data.product_condition"},{"name":"box_condition","field":"data.box_condition"}],"values":{"min_regional_instant_ship_price":{"field":"data.gp_instant_ship_lowest_price_cents_2","aggregation":"min"},"min_regional_price":{"field":"data.gp_lowest_price_cents_2","aggregation":"min"}}}',
    }
    
    while True:
        resp = session.get(url, params=params)
        print(resp.url)

        json_dict = resp.json()

        per_page = json_dict.get("request", dict()).get("num_results_per_page")

        results = json_dict.get("response", dict()).get("results", [])

        for result_dict in results:
            slug = result_dict.get("data", dict()).get("slug")
            
            yield slug

        if len(results) < per_page:
            break

        page += 1

        params['page'] = str(page)

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("{} <query>".format(sys.argv[0]))
        return

    query = sys.argv[1]

    session = create_session()

    out_f = open("results.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for slug in scrape_search(session, query):
        print(slug)

        template_data = get_product_template_data(session, slug)

        template_id = template_data.get("id")
        name = template_data.get("name")
        img_url = template_data.get("mainPictureUrl")
        brand = template_data.get("sizeBrand")
        sku = template_data.get("sku")

        buy_bar_data = get_buy_bar_data(session, slug)

        for buy_bar_dict in buy_bar_data:
            box_condition = buy_bar_dict.get("boxCondition")
            shoe_condition = buy_bar_dict.get("shoeCondition")
            size = buy_bar_dict.get("sizeOption", dict()).get("value")
            stock_status = buy_bar_dict.get("stockStatus")
            lowest_price = buy_bar_dict.get("lowestPriceCents", dict()).get("amount")
            if type(lowest_price) == int:
                lowest_price = lowest_price / 100.0

            row = {
                "template_id": template_id,
                "slug": slug,
                "name": name,
                "img_url": img_url,
                "brand": brand,
                "sku": sku,
                "box_condition": box_condition,
                "shoe_condition": shoe_condition,
                "size": size,
                "stock_status": stock_status,
                "lowest_price": lowest_price
            }

            pprint(row)

            csv_writer.writerow(row)

    out_f.close()

if __name__ == "__main__":
    main()
