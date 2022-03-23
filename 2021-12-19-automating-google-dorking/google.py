#!/usr/bin/python3

import csv
from pprint import pprint

import requests

SEARCH_ENGINE_ID = "[REDACTED]"
API_KEY = "[REDACTED]"

FIELDNAMES = ["query", "result_url", "result_title", "result_snippet"]


def main():
    in_f = open("queries.txt", "r", encoding="utf-8")
    out_f = open("results.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for query in in_f:
        query = query.strip()
        print(query)

        params = {
            "cx": SEARCH_ENGINE_ID,
            "key": API_KEY,
            "q": query,
        }

        resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
        print(resp.url)

        json_dict = resp.json()

        for item_dict in json_dict.get("items", []):
            row = {
                "query": query,
                "result_url": item_dict.get("link"),
                "result_title": item_dict.get("title"),
                "result_snippet": item_dict.get("snippet"),
            }

            pprint(row)

            csv_writer.writerow(row)

    out_f.close()
    in_f.close()


if __name__ == "__main__":
    main()
