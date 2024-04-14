#!/usr/bin/python3

import asyncio
from playwright.sync_api import sync_playwright, Playwright

# $ pip3 install playwright

from pprint import pprint

USERNAME = "[REDACTED]"
PASSWORD = "[REDACTED]"

AUTH = USERNAME + ":" + PASSWORD
SBR_WS_CDP = f"wss://{AUTH}@brd.superproxy.io:9222"


async def run(pw):
    print("Connecting to Scraping Browser...")
    browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        print("Connected! Navigating...")
        page = await browser.new_page()
        await page.goto("https://clutch.co/", timeout=1 * 60 * 1000)
        cookies = await page.context.cookies()
        pprint(cookies)
    except Exception as e:
        print(e)
    finally:
        await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == "__main__":
    asyncio.run(main())
