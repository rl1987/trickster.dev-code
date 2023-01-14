#!/usr/bin/python3

import csv
import sys

import requests

FIELDNAMES = ["symbol", "timestamp", "open", "close", "high", "low", "url"]


def main():
    if len(sys.argv) != 4:
        print("Usage:")
        print("{} <symbol> <interval> <range>".format(sys.argv[0]))
        return 0

    symbol = sys.argv[1]
    interval = sys.argv[2]
    range_ = sys.argv[3]

    if not range_ in [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "ytd",
        "max",
    ]:
        print("Error: Invalid range")
        return -1

    params = {
        "region": "US",
        "lang": "en-US",
        "includePrePost": False,
        "interval": interval,
        "useYfid": True,
        "range": range_,
        "corsDomain": "finance.yahoo.com",
        ".tsrc": "finance",
    }

    url = "https://query1.finance.yahoo.com/v8/finance/chart/" + symbol

    resp = requests.get(
        url,
        params=params,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        },
    )
    print(resp.url)

    result_dict = resp.json().get("chart", dict()).get("result")[0]
    timestamps = result_dict.get("timestamp")
    quote_dict = result_dict.get("indicators").get("quote")[0]
    open_prices = quote_dict.get("open")
    close_prices = quote_dict.get("close")
    high_prices = quote_dict.get("high")
    low_prices = quote_dict.get("low")

    out_f = open(symbol + ".csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for i in range(len(timestamps)):
        row = {
            "symbol": symbol,
            "timestamp": timestamps[i],
            "open": open_prices[i],
            "close": close_prices[i],
            "high": high_prices[i],
            "low": low_prices[i],
            "url": resp.url,
        }

        csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()
