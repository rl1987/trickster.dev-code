#!/usr/bin/python3

import csv
import json
import time
from pprint import pprint

import requests

API_TOKEN = None

def check_if_present(store_name, title, asin):
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': API_TOKEN
    }
    
    api_url = "https://{}.myshopify.com/admin/api/2022-04/products.json".format(store_name)
    
    params = {
        'title': title
    }

    resp = requests.get(api_url, headers=headers, params=params, timeout=10)
    
    json_dict = resp.json()

    if json_dict.get("products") is None or len(json_dict.get("products")) == 0:
        return False

    for prod_dict in json_dict.get("products"):
        variant = prod_dict.get("variants")[0]
        if variant.get("sku") == asin:
            return True

    return False

def import_product(store_name, product):
    headers = {
        'Content-Type': 'application/json',
        'X-Shopify-Access-Token': API_TOKEN
    }
    
    api_url = "https://{}.myshopify.com/admin/api/2022-04/products.json".format(store_name)

    payload = {
        'product': {
            'title': product.get('title'),
            'body_html': product.get('product_details'),
            'vendor': product.get('brand', '').replace("Visit the ", "").replace(" Store", ""),
            'tags': product.get('breadcrumbs', '').split("/"),
            'published': True,
            'options': [
                {'name': 'Size'},
            ],
            'product_type': 'Shoes',
            'images': [],
            'variants': [
                {
                    'sku': product.get('asin'),
                    'price': product.get('price').split(" - ")[-1].replace("£", ""),
                    'requires_shipping': True,
                }
            ],
        }
    }

    i = 1

    for img_url in json.loads(product.get('images_list')):
        payload['product']['images'].append({
            'src': img_url,
            'position': i,
        })

        i += 1

    pprint(payload)

    resp = requests.post(api_url, headers=headers, json=payload, timeout=10)

    if resp.status_code != 201:
        print("Error: Import to shopify failed!")
        print(resp.text)
        return


def main():
    global API_TOKEN

    store_name = input("Enter store name (part of subdomain before .myshopify.com): ")

    t_f = open("api_token.txt", "r")
    API_TOKEN = t_f.read()
    t_f.close()

    in_f = open("amazon_uk_shoes_dataset.csv", "r")

    csv_reader = csv.DictReader(in_f)
    
    for row in csv_reader:
        if row.get("price") == "":
            continue

        if not check_if_present(store_name, row.get('title'), row.get('asin')):
            import_product(store_name, row)
        else:
            print("{} ({}) already present - skipping...".format(row.get('title'), 
                row.get('asin')))

        time.sleep(0.5)

    in_f.close()


if __name__ == "__main__":
    main()

