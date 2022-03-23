#!/usr/bin/python3

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    for url in ["https://www.stockx.com", "https://ifconfig.me"]:
        for browser_type in [p.chromium, p.firefox, p.webkit]:
            browser = p.chromium.launch()
            page = browser.new_page()
            # page = browser.new_page("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36")
            page.goto(url)
            print(page.title())
            domain = url.split("//")[-1]
            page.screenshot(path=f'example-{domain}-{browser_type.name}.png')
            browser.close()
