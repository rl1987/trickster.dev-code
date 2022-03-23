#!/usr/bin/python3

import csv
import configparser
from pprint import pprint
import time

import requests

FIELDNAMES = [ "name", "description", "html_url", "contributors_url" ]

def create_session():
    session = requests.Session()

    config = configparser.ConfigParser()
    config.read('harvest.ini')

    token = config['GH']['Token']

    session.headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token ' + token,
        'User-Agent': 'GithubEmailHarvest',
    }

    return session

def main():
    language = input("Language [Python]: ")
    query = input("Query: ")

    if language == "":
        language = "Python"
    
    session = create_session()

    page = 1
    
    q = '{} language:{}'.format(query, language)

    out_f = open("repos.csv", "w+", encoding="utf-8")
    
    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    while True:
        params = {
            'q': q,
            'page' : str(page),
        }

        resp = session.get('https://api.github.com/search/repositories', params=params)
        print(resp.url)
        print(resp.headers)

        json_dict = resp.json()

        items = json_dict.get('items')
        if items is None or len(items) == 0:
            pprint(json_dict)
            break

        for item_dict in items:
            row = {
                "name" : item_dict.get("name"),
                "description" : item_dict.get("description"),
                "html_url" : item_dict.get("html_url"),
                "contributors_url" : item_dict.get("contributors_url"),
            }

            pprint(row)

            csv_writer.writerow(row)
        
        page += 1
        
        time.sleep(1.2)

    out_f.close()

if __name__ == "__main__":
    main()

