import requests

cookies = {
    "ASP.NET_SessionId": "5zbmmioup1jtvyidmrllbk3y",
    "DISCLAIMER": "1",
}

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'ASP.NET_SessionId=5zbmmioup1jtvyidmrllbk3y; DISCLAIMER=1',
    "Origin": "https://publicaccess.claytoncountyga.gov",
    "Referer": "https://publicaccess.claytoncountyga.gov/search/advancedsearch.aspx?mode=advanced",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
}

params = {
    "mode": "advanced",
}

data = {
    "__VIEWSTATE": [
        "QL5SNhNFfFnBb7b4DtyY96KtZfoOELZgX2ocZ3TbFJ8fXXjiFrP3YoMdN4tbQaFgYrpi6YXyRLBB9cKrBja45rqOV01nCJfwqYr4yiFy/Y/lSjsDmB0sSZZukGHaj+eSsUOrYYI+0nxrQ8KQGBtbq5z1x562R6okx9cJpEJBwbF3evV2qMPQrbSYljFVDWthUtuY79VM57peH1hltn/jd9mPKHphbUlLfdJPTYalCjOG0b1+55I98Z9m1Yo/ZmlRPyC0dNEpZ1NXuVmZ5CYysmWLs0rCUT0ISpZZ436liV5M8Na/dE09bwFkWXoFgqmWU2ldxR+GnDew5ZpJtlizmldcRyuqgNX33kWGEjjW/Y9e/uqdX1ZgdizzSHagwblv0+mGikZ4uzo6pzatN21staAOBMUNxxuiqAQBCX/zpn54LPqvhkqWDyyCk4cVd/87jGmHCdYaHA15048FeoHCG3Ra101+6CHalur7VldWA5pu288tbGCTWhxSLknohMlDWPsrvoLRrVdBZhh0eQavoEdsqJiLGili1+4aKEsdch6IpgE3/W2KnecseGhfvlT132Tq9mUHjWVEuLYbm7LwhQ=="
    ],
    "__VIEWSTATEGENERATOR": ["81E50120"],
    "__EVENTVALIDATION": [
        "OfiCDrhk/7nBQXu+F7/HpdUOvmDSTUs9qP2MZPIOh6agOkKfNTT1BAGpbZLQqe7QUUBuOkvT1uFiIdGa3n9JVkt10MXdyH09K3Xzy7sh7iE4nKhMde815zPrMoxtRwDniItUNoxNJwJ/FszKmejvkRpL5gAK8XpakkBbrfV2kwC7IA8TCDv1KHZAmZcvNptUiGCHCACjOZepl24QvvFP3IbhFWH8kaYQVgqETSHGHWmFgTuaU9X41uYABa6y0+plTPSBbAscfodjbOwQps81L80ZXFvCc0ZmqEgYa0ex7h5ytK74Z82HRvbhDy4HpQNa5CD794vkI8gFqAlv0so5Mb7gGSGN0y+dAhkWpq9euuZn8IVM34gjFk/WUp3SW/A3QHeM7H6U7dpO0sqvOcQZ/Aao/F3v5R0otHgA7loURTzgTq2kuDqsc4jwdMI8NJH/3e9b25e1jPNc0+KLubSEA1rr4r8HOrU6wLjmn7XNpMfGLPyoy//gN8PdAG4ZAXeeUPaT1F/S1TMox3XIqgd9xkUsn3R4ZeeGN/EaEXdLUTs="
    ],
    "SortBy": ["PARID"],
    "SortDir": [" asc"],
    "PageSize": ["15"],
    "hdCriteria": ["price|1000000~2000000"],
    "hdCriteriaTypes": ["N|N|C|C|C|N|C|C|N|D|N|N|C|C|C|N|N"],
    "hdLastState": ["1"],
    "hdSelectedQuery": ["0"],
    "hdSearchType": ["AdvSearch"],
    "hdCriterias": [
        "taxyr|bathrooms|bedrooms|Class|luc|sfla|nbhd|owner|price|salesdate|com_sf|stories|adrstr|style|taxdist|yr_com|yr_buitl"
    ],
    "hdSelectAllChecked": ["false"],
    "sCriteria": ["9"],
    "ctl01_cal1_dateInput_ClientState": [
        '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00","lastSetTextBoxValue":""}'
    ],
    "ctl01_cal1_calendar_SD": ["[]"],
    "ctl01_cal1_calendar_AD": ["[[1900,1,1],[2099,12,30],[2022,5,1]]"],
    "ctl01_cal1_ClientState": [
        '{"minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00"}'
    ],
    "txtCrit": ["1000000"],
    "ctl01_cal2_dateInput_ClientState": [
        '{"enabled":true,"emptyMessage":"","validationText":"","valueAsString":"","minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00","lastSetTextBoxValue":""}'
    ],
    "ctl01_cal2_calendar_SD": ["[]"],
    "ctl01_cal2_calendar_AD": ["[[1900,1,1],[2099,12,30],[2022,5,1]]"],
    "ctl01_cal2_ClientState": [
        '{"minDateStr":"1900-01-01-00-00-00","maxDateStr":"2099-12-31-00-00-00"}'
    ],
    "txtCrit2": ["2000000"],
    "txCriterias": ["9"],
    "selSortBy": ["PARID"],
    "selSortDir": [" asc"],
}

response = requests.post(
    "https://publicaccess.claytoncountyga.gov/search/advancedsearch.aspx",
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)

print(response)

assert "LGS HOLDING GROUP 2013 LLC" in response.text
