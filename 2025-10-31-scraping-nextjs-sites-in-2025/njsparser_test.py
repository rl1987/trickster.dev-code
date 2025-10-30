import requests
import njsparser
from pprint import pprint

proxy_url = input("Proxy URL: ")

if proxy_url.strip() == "":
    proxy_url = None

proxies = {
    "https": proxy_url
}

url = input("Page URL: ")

response = requests.get(url, proxies=proxies, verify=False)
print(response.url, response.status_code)

fd = njsparser.BeautifulFD(response.text)
for data in fd.find_iter([njsparser.T.Data, njsparser.T.Element]):
    print(type(data))
    pprint(data)
