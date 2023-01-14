#!/usr/bin/python3

import csv
from pprint import pprint

import requests
from lxml import html

FIELDNAMES = [
    "ticker",
    "prev_close",
    "open",
    "bid",
    "ask",
    "days_range",
    "52_wk_range",
    "volume",
    "avg_volume",
    "market_cap",
    "beta",
    "pe",
    "eps",
    "earnings_date",
    "fw_dividend_and_yield",
    "ex_dividend_date",
    "1y_target_est",
    "url",
]


def scrape_summary(ticker):
    url = "https://finance.yahoo.com/quote/" + ticker

    xpath_by_field = {
        "prev_close": '//td[@data-test="PREV_CLOSE-value"]/text()',
        "open": '//td[@data-test="OPEN-value"]/text()',
        "bid": '//td[@data-test="BID-value"]/text()',
        "ask": '//td[@data-test="ASK-value"]/text()',
        "days_range": '//td[@data-test="DAYS_RANGE-value"]/text()',
        "52_wk_range": '//td[@data-test="FIFTY_TWO_WK_RANGE-value"]/text()',
        "volume": '//td[@data-test="TD_VOLUME-value"]/fin-streamer/text()',
        "avg_volume": '//td[@data-test="AVERAGE_VOLUME_3MONTH-value"]/text()',
        "market_cap": '//td[@data-test="MARKET_CAP-value"]/text()',
        "beta": '//td[@data-test="BETA_5Y-value"]/text()',
        "pe": '//td[@data-test="PE_RATIO-value"]/text()',
        "eps": '//td[@data-test="EPS_RATIO-value"]/text()',
        "earnings_date": '//td[@data-test="EARNINGS_DATE-value"]/span/text()',
        "fw_dividend_and_yield": '//td[@data-test="DIVIDEND_AND_YIELD-value"]/text()',
        "ex_dividend_date": '//td[@data-test="EX_DIVIDEND_DATE-value"]//text()',
        "1y_target_est": '//td[@data-test="ONE_YEAR_TARGET_PRICE-value"]/text()',
    }

    row = {"ticker": ticker, "url": url}

    resp = requests.get(url)
    print(resp.url)

    tree = html.fromstring(resp.text)

    for f in xpath_by_field.keys():
        try:
            row[f] = tree.xpath(xpath_by_field[f])[0]
        except Exception as e:
            print(f)
            print(e)

    return row


def main():
    in_f = open("tickers.txt", "r")
    tickers = in_f.read().strip().split("\n")
    in_f.close()

    out_f = open("summary.csv", "w", encoding="utf-8")
    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    for ticker in tickers:
        row = scrape_summary(ticker)
        if row is not None:
            pprint(row)
            csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()
