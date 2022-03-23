#!/usr/bin/python3

import csv
from datetime import datetime
from pprint import pprint
import sys

import praw

USER_AGENT = "automations"

FIELDNAMES = [ "subreddit", "username", "title", "selftext", "datetime" ]
OUTPUT_CSV_PATH = "posts.csv"

def iso_timestamp_from_unix_time(unix_time):
    dt = datetime.fromtimestamp(unix_time)
    return dt.isoformat()

def scrape_subreddit(reddit, query, subreddit_name):
    sr = reddit.subreddit(display_name=subreddit_name)

    for s in sr.search(query, limit=None):
        row = {
            "subreddit": subreddit_name,
            "username" : s.author.name,
            "title": s.title,
            "selftext": s.selftext.replace("\n", " "),
            "datetime": iso_timestamp_from_unix_time(s.created_utc),
        }

        yield row

def main():
    if len(sys.argv) != 3:
        print("{} <query> <subreddit1,subreddit2,...>".format(sys.argv[0]))
        print("Use subreddit names with /r/ - e.g. 'webscraping', not '/r/webscraping'")
        return

    query = sys.argv[1]
    subreddit_names = sys.argv[2].split(",")

    reddit = praw.Reddit("bot", user_agent=USER_AGENT)

    out_f = open(OUTPUT_CSV_PATH, "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for subreddit_name in subreddit_names:
        for row in scrape_subreddit(reddit, query, subreddit_name):
            pprint(row)

            csv_writer.writerow(row)

    out_f.close()
    
if __name__ == "__main__":
    main()
