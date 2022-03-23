#!/usr/bin/python3

import json
import time

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    c_f = open("cookies.json", "r")
    cookies = json.load(c_f)
    c_f.close()

    context.add_cookies(cookies)

    # Open new page
    page = context.new_page()

    # Go to https://www.instagram.com/
    page.goto("https://www.instagram.com/")

    time.sleep(10)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
