#!/usr/bin/python3

import logging
import json
import uuid

import requests
import websocket

MATCH_STR = "!test"
RESPONSE = "Hey there!"

TWITCH_USERNAME = "[REDACTED]"
TWITCH_PASSWORD = "[REDACTED]"
CHANNEL_NAME = "[REDACTED]"
GQL_API_URL = "https://gql.twitch.tv/gql"

def login_to_twitch(username, password):
    session = requests.Session()

    session.headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8,lt;q=0.7",
    }

    resp1 = session.get("https://www.twitch.tv/directory")

    session.cookies.set(
        "api_token", "twilight.46cc59eee010864b5ddfa5bc17f457b8", domain="twitch.tv"
    )
    logging.debug(session.cookies)

    payload = {
        "username": username,
        "password": password,
        "client_id": "kimne78kx3ncx6brgo4mv6wki5h1ko",
        "undelete_user": False,
    }

    logging.debug(payload)
    resp2 = session.post("https://passport.twitch.tv/login", json=payload)
    logging.debug(resp2.text)

    json_dict = resp2.json()

    token = json_dict.get("access_token")

    if json_dict.get("error_code") == 3022:
        err_msg = json_dict.get("error")
        logging.error(err_msg)
        captcha_proof = json_dict.get("captcha_proof")
        code = input("Code from email ({}): ".format(json_dict.get("obscured_email")))
        code = code.strip()

        payload["captcha"] = {"proof": captcha_proof}
        payload["twitchguard_code"] = code

        logging.debug(payload)
        resp3 = session.post("https://passport.twitch.tv/login", json=payload)

        logging.debug(resp3.text)

        json_dict = resp3.json()

        token = json_dict.get("access_token")

    session.headers["Client-Id"] = "kimne78kx3ncx6brgo4mv6wki5h1ko"

    if token is not None:
        session.headers["Authorization"] = "OAuth {}".format(token)

    return session, token

def get_channel_id(session, channel):
    logging.info("Retrieving ID for channel {}".format(channel))

    payload = {
        "operationName": "PlaybackAccessToken",
        "variables": {
            "isLive": True,
            "login": channel.replace("#", ""),
            "isVod": False,
            "vodID": "",
            "playerType": "site",
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "0828119ded1c13477966434e15800ff57ddacf13ba1911c129dc2200705b0712",
            }
        },
    }

    logging.debug(payload)
    resp = session.post(GQL_API_URL, json=payload)
    logging.debug(resp.text)

    json_dict = resp.json()

    value_str = json_dict.get("data", dict()).get("streamPlaybackAccessToken", dict()).get("value")
    if value_str is None:
        return
        
    value_dict = json.loads(value_str)

    channel_id = value_dict.get("channel_id")

    if channel_id is not None:
        logging.info(
            "Got channel ID for {} : {}".format(channel, channel_id)
        )

        return channel_id

    return None

def follow_channel(session, channel_id):
    payload = [
        {
            "operationName": "FollowButton_FollowUser",
            "variables": {
                "input": {
                    "disableNotifications": False,
                    "targetID": str(channel_id),
                }
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "800e7346bdf7e5278a3c1d3f21b2b56e2639928f86815677a7126b093b2fdd08",
                }
            },
        }
    ]

    logging.debug(payload)
    resp = session.post(GQL_API_URL, json=payload)
    logging.debug(resp.text)

def connect_to_websocket(username, channel, token):
    ws = websocket.WebSocket()
    ws.connect(
        "wss://irc-ws.chat.twitch.tv/",
    )

    ws.send("CAP REQ :twitch.tv/tags twitch.tv/commands")
    ws.send("PASS oauth:{}".format(token))
    ws.send("NICK {}".format(username))
    ws.send("USER {} 8 * :{}".format(username, username))
    ws.send("JOIN {}".format(channel))

    return ws

def send_message(ws, channel, message):
    nonce = str(uuid.uuid4()).replace("-", "")

    ws.send("@client-nonce={} PRIVMSG {} :{}".format(nonce, channel, message))

def run_loop(ws, channel, match_str, response):
    while True:
        try:
            message = ws.recv()
        except Exception as e:
            logging.warning(e)
            break

        logging.debug(message)
        if message.startswith("PING"):
            ws.send("PONG")
        elif "PRIVMSG {} :".format(channel) in message:
            message = message.split("PRIVMSG {} :".format(channel))[-1]
            if match_str in message:
                send_message(ws, channel, response)

def main():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        level=logging.DEBUG,
    )

    websocket.enableTrace(True)

    session, token = login_to_twitch(TWITCH_USERNAME, TWITCH_PASSWORD)

    channel_id = get_channel_id(session, CHANNEL_NAME)
    
    follow_channel(session, channel_id)

    ws = connect_to_websocket(TWITCH_USERNAME, CHANNEL_NAME, token)
    
    run_loop(ws, CHANNEL_NAME, MATCH_STR, RESPONSE)

if __name__ == "__main__":
    main()
