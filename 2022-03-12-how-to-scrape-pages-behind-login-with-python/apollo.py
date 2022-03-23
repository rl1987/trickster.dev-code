#!/usr/bin/python3

import csv
from pprint import pprint
import time
import string
import random

import requests


def create_session(username, password):
    session = requests.Session()

    session.headers = {
        "authority": "app.apollo.io",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36",
        "sec-ch-ua-platform": '"macOS"',
        "accept": "*/*",
        "origin": "https://app.apollo.io",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://app.apollo.io/",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    }

    json_data = {
        "email": username,
        "password": password,
        "timezone_offset": 0,
        "cacheKey": int(time.time()),
    }

    pprint(json_data)

    response = session.post("https://app.apollo.io/api/v1/auth/login", json=json_data)
    print(response.url)

    json_dict = response.json()

    view_id = (
        json_dict.get("bootstrapped_data", dict()).get("finder_views")[0].get("id")
    )

    return session, view_id


def scrape_company_data(session, view_id, query, output_csv_path):
    page = 1

    json_data = {
        "finder_view_id": view_id,
        "q_organization_name": query,
        "page": page,
        "display_mode": "explorer_mode",
        "per_page": 25,
        "open_factor_names": [],
        "num_fetch_result": 1,
        "context": "companies-index-page",
        "show_suggestions": False,
        # Based on:
        # https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
        "ui_finder_random_seed": "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(6)
        ),
        "cacheKey": int(time.time()),
    }

    out_f = open(output_csv_path, "w", encoding="utf-8")
    csv_writer = csv.DictWriter(
        out_f,
        fieldnames=["name", "linkedin_url", "website_url", "primary_domain", "phone"],
        lineterminator="\n",
    )
    csv_writer.writeheader()

    while True:
        resp = session.post(
            "https://app.apollo.io/api/v1/mixed_companies/search", json=json_data
        )
        print(resp.url)

        json_dict = resp.json()

        for org_dict in json_dict.get("organizations", []):
            name = org_dict.get("name")
            linkedin_url = org_dict.get("linkedin_url")
            website_url = org_dict.get("website_url")
            primary_domain = org_dict.get("primary_domain")
            phone = org_dict.get("phone")

            row = {
                "name": name,
                "linkedin_url": linkedin_url,
                "website_url": website_url,
                "primary_domain": primary_domain,
                "phone": phone,
            }

            pprint(row)
            csv_writer.writerow(row)

        pagination_dict = json_dict.get("pagination")
        total_pages = pagination_dict.get("total_pages")

        if total_pages == page:
            break

        page += 1
        json_data["page"] = page

    out_f.close()


def main():
    username = input("Username: ")
    password = input("Password: ")

    query = input("Search query: ")
    output_csv_path = input("Output CSV path: ")

    session, view_id = create_session(username, password)

    print(session.cookies)

    scrape_company_data(session, view_id, query, output_csv_path)


if __name__ == "__main__":
    main()
