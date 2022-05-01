import requests

cookies = {
    "DISCLAIMER": "1",
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
    "txtCrit": ["1000000"],
    "txtCrit2": ["2000000"],
    "txCriterias": ["9"],
    "selSortBy": ["PARID"],
    "selSortDir": [" asc"],
}

response = requests.post(
    "https://publicaccess.claytoncountyga.gov/search/advancedsearch.aspx",
    params=params,
    cookies=cookies,
    data=data,
)

print(response)

assert "LGS HOLDING GROUP 2013 LLC" in response.text
