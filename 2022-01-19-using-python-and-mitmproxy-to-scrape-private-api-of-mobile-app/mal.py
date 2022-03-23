#!/usr/bin/python3

import csv
from pprint import pprint

import requests

FIELDNAMES = ["title", "synopsis", "status", "genres", "mean"]


def main():
    out_f = open("cur_season.csv", "w", encoding="utf-8")
    csv_writer = csv.DictWriter(out_f, fieldnames=FIELDNAMES, lineterminator="\n")
    csv_writer.writeheader()

    headers = {
        "accept": "*/*",
        "x-mal-client-id": "6591a087c62b3e94d769cd8e35ffe909",
        "cache-control": "public, max-age=60",
        "user-agent": "MAL (ios, 139)",
        "accept-language": "en-GB,en;q=0.9",
    }

    resp1 = requests.get("https://api.myanimelist.net/v3/anime/season", headers=headers)
    print(resp1.url)

    json_dict = resp1.json()

    season = None
    year = None

    for season_dict in json_dict.get("data", []):
        node_dict = season_dict.get("node", dict())
        if node_dict.get("is_current"):
            season = node_dict.get("season")
            year = node_dict.get("year")
            break

    params = {
        "fields": "alternative_titles,media_type,genres,num_episodes,status,start_date,end_date,average_episode_duration,synopsis,mean,rank,popularity,num_list_users,num_favorites,num_scoring_users,start_season,broadcast,my_list_status{start_date,finish_date},favorites_info,nsfw,created_at,updated_at",
        "limit": "50",
        "media_type": "tv",
        "offset": "0",
        "sort": "anime_num_list_users",
        "start_season_season": season,
        "start_season_year": str(year),
    }

    resp2 = requests.get(
        "https://api.myanimelist.net/v3/anime", headers=headers, params=params
    )
    print(resp2.url)

    json_dict = resp2.json()

    for show_dict in json_dict.get("data", []):
        node_dict = show_dict.get("node", dict())

        if node_dict.get("genres") is not None:
            genres = list(map(lambda g: g.get("name"), node_dict.get("genres")))
        else:
            genres = []

        row = {
            "title": node_dict.get("title"),
            "synopsis": node_dict.get("synopsis", "").replace("\n", " "),
            "status": node_dict.get("status"),
            "genres": ",".join(genres),
            "mean": node_dict.get("mean"),
        }

        pprint(row)

        csv_writer.writerow(row)

    out_f.close()


if __name__ == "__main__":
    main()

