#!/usr/bin/python3

import requests

def find_chat_ids(token):
    chat_ids = set()

    url = "https://api.telegram.org/bot{}/getUpdates".format(token)

    resp = requests.get(url)

    json_dict = resp.json()

    results = json_dict.get("result", [])

    for rd in results:
        chat_id = rd.get("message", dict()).get("chat", dict()).get("id")
        chat_ids.add(chat_id)

    return list(chat_ids)

def main():
    token = "[REDACTED]"

    for chat_id in find_chat_ids(token):
        data = {"chat_id": chat_id, "text": message}

        url = "https://api.telegram.org/bot{}/sendMessage".format(token)

        resp = requests.post(url, data=data)

if __name__ == "__main__":
    main()

