#!/usr/bin/python3

import tls_client
from playwright.sync_api import sync_playwright, Playwright

USERNAME = "[REDACTED]"
PASSWORD = "[REDACTED]"
PROXY_URL = "[REDACTED]"

AUTH = USERNAME + ":" + PASSWORD
SBR_WS_CDP = f"wss://{AUTH}@brd.superproxy.io:9222"


def get_cookies(page_url):
    cookies = None

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(SBR_WS_CDP)
        try:
            page = browser.new_page()
            page.goto(page_url, timeout=1 * 60 * 1000)
            cookies = page.context.cookies()
            print("Got cookies:", cookies)
        except Exception as e:
            print(e)
        finally:
            browser.close()

    return cookies


def create_session(page_url):
    session = tls_client.Session(
        client_identifier="chrome120", random_tls_extension_order=True
    )

    session.headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36",
    }

    cookies = get_cookies(page_url)

    for cookie in cookies:
        session.cookies.set(
            cookie.get("name"), cookie.get("value"), domain=cookie.get("domain")
        )

    session.proxies = {"http": PROXY_URL, "https": PROXY_URL}

    return session

N_RETRIES = 5

def safe_get(session, url):
    retries_left = N_RETRIES

    while retries_left > 0:
        try:
            resp = session.get(url)
            return resp
        except Exception as e:
            print(e)
            print("Retrying: {}".format(url))
            retries_left -= 1
    
    return None

