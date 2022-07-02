#!/usr/bin/python3

import csv
import sys

import requests
from lxml import html
import js2xml


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("{} <youtube_url>".format(sys.argv[0]))
        return

    url = sys.argv[1]

    out_f = open("view_intensity.csv", "w", encoding="utf-8")

    csv_writer = csv.DictWriter(
        out_f, fieldnames=["time", "intensity", "url"], lineterminator="\n"
    )
    csv_writer.writeheader()

    resp = requests.get(url)
    print(resp.url)

    tree = html.fromstring(resp.text)
    initial_data_js = tree.xpath(
        '//script[starts-with(text(), "var ytInitialData = ")]/text()'
    )
    initial_data_js = initial_data_js[0]

    parsed = js2xml.parse(initial_data_js)

    for hmr in parsed.xpath('//property[@name="heatMarkerRenderer"]'):
        start = hmr.xpath('.//property[@name="timeRangeStartMillis"]/number/@value')[0]
        score = hmr.xpath(
            './/property[@name="heatMarkerIntensityScoreNormalized"]/number/@value'
        )[0]
        print(start, score)

        csv_writer.writerow({"time": start, "intensity": score, "url": url})

    out_f.close()


if __name__ == "__main__":
    main()
