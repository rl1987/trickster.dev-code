#!/usr/bin/python3

from playwright.sync_api import sync_playwright, Playwright

from pprint import pprint

USERNAME = "[REDACTED]"
PASSWORD = "[REDACTED]"

AUTH = USERNAME + ":" + PASSWORD
SBR_WS_CDP = f"wss://{AUTH}@brd.superproxy.io:9222"


def run(pw: Playwright):
    browser = pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        page = browser.new_page()
        page.goto("https://clutch.co", timeout=1 * 60 * 1000)
        cookies = page.context.cookies()
        pprint(cookies)
    except Exception as e:
        print(e)
    finally:
        browser.close()


def main():
    with sync_playwright() as playwright:
        run(playwright)


if __name__ == "__main__":
    main()
