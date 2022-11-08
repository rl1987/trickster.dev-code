#!/usr/bin/python3

import multiprocessing
import logging
import subprocess
import json
import os
import sys

spider_name = None


def run_scrapy_subprocess(year, month):
    csv_filename = "{}-{}-{}.csv".format(spider_name, year, month)
    if os.path.isfile(csv_filename):
        os.unlink(csv_filename)

    log_filename = "scrapy-{}-{}.log".format(year, month)
    if os.path.isfile(log_filename):
        os.unlink(log_filename)

    stats_filename = "stats-{}-{}.json".format(year, month)

    cmd = [
        "scrapy",
        "runspider",
        "-o",
        csv_filename,
        "--logfile",
        log_filename,
        "housingprices/spiders/{}.py".format(spider_name),
        "-a",
        "year={}".format(year),
        "-a",
        "month={}".format(month),
        "-a",
        "stats_filepath={}".format(stats_filename),
    ]

    print(cmd)

    result = subprocess.run(cmd)
    if result.returncode != 0:
        return False

    json_f = open(stats_filename, "r")
    stats = json.load(json_f)
    json_f.close()

    if stats.get("log_count/ERROR") is not None:
        return False

    if (
        stats.get("downloader/response_status_count/500") is not None
        and stats.get("downloader/response_status_count/500") > 8
    ):
        return False

    if (
        stats.get("downloader/response_status_count/501") is not None
        and stats.get("downloader/response_status_count/501") > 8
    ):
        return False

    return True


def perform_task(shard):
    year, month = shard
    print("Year: {}, month: {}".format(year, month))

    while True:
        success = run_scrapy_subprocess(year, month)
        if success:
            print("{} {} succeeded".format(year, month))
            break

        print("{} {} failed - retrying".format(year, month))


def main():
    global spider_name

    if len(sys.argv) != 2:
        print("Usage:")
        print("{} <spider_name>".format(sys.argv[0]))
        return

    spider_name = sys.argv[1]

    shards = []

    from_year = 1901
    to_year = 2022

    for year in range(from_year, to_year + 1):
        for month in range(1, 13):
            shard = (year, month)
            shards.append(shard)

    pool = multiprocessing.Pool(32)
    pool.map(perform_task, shards)


if __name__ == "__main__":
    main()
