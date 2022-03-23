#!/usr/bin/python3

import requests
from lxml import html

from anticaptchaofficial.recaptchav2proxyless import *

def main():
    resp1 = requests.get("https://www.google.com/recaptcha/api2/demo")

    tree = html.fromstring(resp1.text)

    sitekey = tree.xpath('//div[@id="recaptcha-demo"]/@data-sitekey')[0]

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key("[REDACTED]")
    solver.set_website_url(resp1.url)
    solver.set_website_key(sitekey)

    g_response = solver.solve_and_return_solution()

    assert g_response != 0

    form_data = {
        'g-recaptcha-response': g_response
    }

    resp2 = requests.post('https://www.google.com/recaptcha/api2/demo', data=form_data)

    print(resp2.text)


if __name__ == "__main__":
    main()
