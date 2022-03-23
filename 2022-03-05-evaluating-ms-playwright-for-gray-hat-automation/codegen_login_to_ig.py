from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.instagram.com/
    page.goto("https://www.instagram.com/")

    # Click text=Only allow essential cookies
    page.locator("text=Only allow essential cookies").click()

    # Click [aria-label="Phone\ number\,\ username\,\ or\ email"]
    page.locator("[aria-label=\"Phone\\ number\\,\\ username\\,\\ or\\ email\"]").click()

    # Fill [aria-label="Phone\ number\,\ username\,\ or\ email"]
    page.locator("[aria-label=\"Phone\\ number\\,\\ username\\,\\ or\\ email\"]").fill("[REDACTED]")

    # Click [aria-label="Password"]
    page.locator("[aria-label=\"Password\"]").click()

    # Fill [aria-label="Password"]
    page.locator("[aria-label=\"Password\"]").fill("[REDACTED]")

    # Click button:has-text("Log In") >> nth=0
    # with page.expect_navigation(url="https://www.instagram.com/"):
    with page.expect_navigation():
        page.locator("button:has-text(\"Log In\")").first.click()

    # Click text=Not Now
    page.locator("text=Not Now").click()

    cookies = context.cookies()
    import json
    c_f = open("cookies.json", "w")
    json.dump(cookies, c_f)
    c_f.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
