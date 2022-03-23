#!/usr/bin/python3

import json

import requests
from lxml import html


def main():
    resp = requests.get("https://dropservicemafia.com/free-course/")

    tree = html.fromstring(resp.text)

    video_divs = tree.xpath('//div[@data-widget_type="video.default"]')

    out_f = open("urls.txt", "w")

    for video_div in video_divs:
        settings_json = video_div.get("data-settings")
        settings_dict = json.loads(settings_json)

        youtube_url = settings_dict.get("youtube_url")
        if youtube_url is None:
            continue

        out_f.write(youtube_url + "\n")

    out_f.close()


if __name__ == "__main__":
    main()
