#!/usr/bin/python3

from urllib.parse import urlencode
import time
import sys

import pandas as pd

ORIG_URL = "https://doc.iowa.gov/daily-statistics"


def get_snapshot_urls():
    params = {"url": ORIG_URL, "output": "json", "filter": "statuscode:200"}

    cdx_url = "http://web.archive.org/cdx/search/cdx" + "?" + urlencode(params)

    print(cdx_url)

    df = pd.read_json(cdx_url)

    headers = df.iloc[0]
    df = pd.DataFrame(df.values[1:], columns=headers)

    df["snapshot_url"] = df["timestamp"].apply(
        lambda ts: "https://web.archive.org/web/" + ts + "/https://doc.iowa.gov/"
    )

    return df["snapshot_url"].to_list()


def scrape_stats_table(url):
    dfs = pd.read_html(
        "https://web.archive.org/web/20210303210751/https://doc.iowa.gov/daily-statistics"
    )

    print(url)

    stats_df = dfs[1]
    stats_df = stats_df[["Institution", "Current Count"]]
    stats_df = stats_df[:-2]
    stats_df.loc[
        stats_df["Institution"] == "Forensic Psychiatric Hospital", "Institution"
    ] = "Oakdale - Forensic Psychiatric Hospital"
    stats_df.loc[stats_df["Institution"] == "Minimum", "Institution"] = "Newton-Minimum"
    stats_df.loc[
        stats_df["Institution"] == "Minimum Live-Out", "Institution"
    ] = "Mitchellville - Minimum Live-Out"
    stats_df["url"] = url

    print(stats_df)

    return stats_df


def main():
    snapshot_urls = get_snapshot_urls()

    print("Found {} snapshots".format(len(snapshot_urls)))

    result_dfs = []

    for url in snapshot_urls:
        try:
            stats_df = scrape_stats_table(url)
        except KeyboardInterrupt:
            sys.exit(1)
        except:
            time.sleep(5)
            try:
                stats_df = scrape_stats_table(url)
            except KeyboardInterrupt:
                sys.exit(1)
            except:
                continue

        result_dfs.append(stats_df)

    result_df = pd.concat(result_dfs)
    result_df.to_csv("iowa_doc.csv", index=False)


if __name__ == "__main__":
    main()
