#!/usr/bin/python3

import csv
import json
from urllib.parse import quote

import requests

# elasticsearch API credentials:
USERNAME = "collections"
PASSWORD = "o41KG!MmJQ$A66"

def create_session():
    session = requests.Session()

    session.headers = {
        'authority': 'collection.carnegieart.org',
        'accept': 'application/json',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://collection.carnegieart.org',
        'pragma': 'no-cache',
        'referer': 'https://collection.carnegieart.org/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }

    session.auth = (USERNAME, PASSWORD)

    return session

def gen_rows_from_response_payload(resp_json):
    hits = resp_json.get('hits', dict()).get('hits', [])

    for hit_dict in hits:
        source_dict = hit_dict.get("_source", dict())

        item = dict()
        
        item["title"] = source_dict.get("title")
        item["department"] = source_dict.get("department")
        item["category"] = source_dict.get("type")
        item["current_location"] = source_dict.get("current_location")
        item["materials"] = source_dict.get("medium")
        item["technique"] = source_dict.get("medium_description")
        item["from_location"] = source_dict.get("creation_address")
        item["date_description"] = source_dict.get("creation_date")[0]

        try:
            item["year_start"] = int(source_dict.get("creation_date")[0])
            item["year_end"] = int(source_dict.get("creation_date")[-1])
        except:
            pass

        makers = source_dict.get("creators", [])
        if makers is not None and len(makers) > 0:
            maker_names = list(map(lambda m: m.get("label"), makers))
            maker_birth_years = list(map(lambda m: str(m.get("birth", "")), makers))
            maker_death_years = list(map(lambda m: str(m.get("death", "")), makers))
            maker_genders = list(map(lambda m: str(m.get("gender")), makers))

            item["maker_full_name"] = "|".join(maker_names)
            item["maker_birth_year"] = "|".join(maker_birth_years).replace("None", "")
            item["maker_death_year"] = "|".join(maker_death_years).replace("None", "")
            item["maker_gender"] = "|".join(maker_genders).replace("None", "")

        try:
            item["acquired_year"] = source_dict.get("acquisition_date", "").split("-")[0]
        except:
            pass

        item["acquired_from"] = source_dict.get("acquisition_method")
        item["accession_number"] = source_dict.get("accession_number")
        item["credit_line"] = source_dict.get("credit_line")

        item["url"] = "https://collection.carnegieart.org/objects/" + source_dict.get("id", "").replace("cmoa:objects/", "")
    
        yield item

def scrape(session):
    json_payload = {
        "query": {
            "match_all": dict()
        },
        "size": 24,
        "from": 0,
        "sort": [
            {
                "acquisition_date": {
                    "order": "desc"
                }
            }
        ],
    }

    params = {
        "scroll": "1m"
    }

    resp0 = session.post("https://collection.carnegieart.org/api/cmoa_objects/_search",
                         json=json_payload, params=params)
    print(resp0.url)

    yield from gen_rows_from_response_payload(resp0.json())

    scroll_id = resp0.json().get('_scroll_id')

    while scroll_id is not None:
        resp = session.get("https://collection.carnegieart.org/api/_search/scroll/" + scroll_id,
                           params=params)
        print(resp.url)

        yield from gen_rows_from_response_payload(resp.json())
        hits = resp.json().get('hits', dict()).get('hits', [])
        if len(hits) == 0:
            break

        scroll_id = resp.json().get('_scroll_id')

def main():
    session = create_session()
 
    out_f = open("carnegie.csv", "w", encoding="utf-8")
    csv_writer = None

    for row in scrape(session):
        print(row)
        if csv_writer is None:
            csv_writer = csv.DictWriter(out_f, fieldnames=list(row.keys()),
                                        lineterminator="\n")
            csv_writer.writeheader()

        csv_writer.writerow(row)

if __name__ == "__main__":
    main()

