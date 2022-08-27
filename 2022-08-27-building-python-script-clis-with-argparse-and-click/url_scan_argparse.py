#!/usr/bin/python3

import argparse
import http.client
import os
import sys
import logging

import requests

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}

DEFAULT_TIMEOUT = 1.0


def check_url(url, timeout):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        return resp.status_code
    except Exception as e:
        return str(e)


def check_urls(urls, timeout, verbose):
    if verbose:
        # Based on: https://stackoverflow.com/a/16630836
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    for u in urls:
        if u.startswith("http://") or u.startswith("https://"):
            print("{}\t{}".format(u, check_url(u, timeout)))
        else:
            if os.path.isfile(u):
                urls_from_file = []
                in_f = open(u, "r")
                lines = in_f.read().strip().split("\n")
                for line in lines:
                    if line.startswith("http://") or line.startswith("https://"):
                        urls_from_file.append(line)
                in_f.close()
                check_urls(urls_from_file, timeout, verbose)
            else:
                print("File not found: {}".format(u), file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Simple HTTP URL Checker")

    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        required=False,
        help="Timeout duration for HTTP GET request in seconds (default: {})".format(
            DEFAULT_TIMEOUT
        ),
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        required=False,
        help="Enable HTTP debug output (off by default)",
    )
    parser.add_argument(
        "--url-list",
        required=True,
        nargs="*",
        help="HTTP URLs or files containing them (one URL per line)",
    )

    args = parser.parse_args(sys.argv[1:])

    check_urls(args.url_list, args.timeout, args.verbose)


if __name__ == "__main__":
    main()
