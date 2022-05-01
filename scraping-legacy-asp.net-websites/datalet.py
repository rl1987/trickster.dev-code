import requests

cookies = {
    "ASP.NET_SessionId": "5zbmmioup1jtvyidmrllbk3y",
    "DISCLAIMER": "1",
}

params = {
    "mode": "advanced",
}

data = {
    "__VIEWSTATE": [
        "xp+U7xWIH/WkG8AjGBqENMMc/lJWzEPo8hVNxOMXvVHVE6DLDW15N7QUlsVAmirgwz3l8N9B2Bao8Krnu1WzlljJr5ULUpOe3FrjCr0ByGJxuYXs8KRohuPMS00PQpVIYnQdeOLaUsr7cm8i2qOmGqgXtLrYRe4PfHO1RezWXMmvuM6LhiA3kZ2SHixuAsXKJC7Y1V7D6j5Ym5magtFXe8GQIG/HSC8uhY6ciEpbHrpCEeDJsXtyuOmk93pBrnvk+nJsWidtubDTPFQSWKwo0J0tH5gvf9ePUjCrJOGKfDzBJ+Y03TPxmBFkDSwX+Lct3N+0gmmYifB9YaZakj1fG90TyuxhXgnmh1xBHTFqQE5ANNBXuBAlyikA6NfDIlg1NWQINT+iLSurkNHLMYpvOPiUT183D5ZYr0l5kMnHFly0ESEbqLyVCcxWOybiaCYiq4zS7/gFWhQ9n59d13y59oJHpyVhGvijTaTSvGaqalY9ZLrV11hiXGh1XQySbJX+t4ku/ioO5IaIYI93Pv8k163sRczbLoNijz5qRFVmtjrrLXAkrZHMZP6s6QBG67W1MSFEQF9Evn5heWX9PR/sfWa6jMeh3jP5u72TZteV8g4="
    ],
    "__VIEWSTATEGENERATOR": ["81E50120"],
    "__EVENTVALIDATION": [
        "JGlJpwTn+zu8GzcJc0cWEZ2W46/xFsJKpBB6bL0XdXJXlE35rX3XiuWLCIFtcxWKdEHUHnOOrPR0aNbsfhqF3DDQJFkV+Lb95S/gn8GigaiPWiB9kTgAR7Al8doUG5V8LLYbpzb9LbDEg3ogCxansImqtx9fEu7usd6IxJWukxLhUor43DuBIGoDXeFIkTCa2ZcPOvfRDulGfsDlI3losFm+SFFiaCan9JgvgBWCJGnctSEd+7K5dGNWootxCprge3JHMN2koEkUx+nHFh8WzcBiwC4uAoYzSgETGI8yImOqYoD4HlW3WC3XgqsWTMU5oC4ICrut5g6fbBl9Y78lMtk0z8tWVyl6KYAT61lzk39hnOjKqtIQDeXYIoBVdqDRarOiaaQD5wIZgc8aUy1wh6auyT3SvnMTLbhBmUF5xKhyczsCjHAON3zbyt2ITbY77QGWx3KCoFkDNW4hLZCmtWXUR5Jpr44UyFK0Gdqfd7v8CQfDi2FyG2pxbdwB3f21ckA0C0cNknAb+tONxXwwhzHz/Nmka7cuzALQgX41oQyVfW2bM/he5G4Lil1M55bCEytG93p3Vw9sx+HeXJb0kVcSh39Q00rLSYUiCM+d3N0op25g35PooLcEE8APdXuA47FkDNyDm0WhqpPgrOjHkrpL/cW6h4OG5SGG+6qhL30wy28FPpPtC/YvADkgH9Jbg6NkFXPCKsrgZM42/z0JZDgrunpVHxHbtxZOy8zgPqk="
    ],
    "PageNum": ["1"],
    "SortBy": ["PARID"],
    "SortDir": [" asc"],
    "PageSize": ["1"],
    "hdAction": ["Link"],
    "hdCriteria": ["price|1000000~2000000"],
    "hdCriteriaTypes": ["N|N|C|C|C|N|C|C|N|D|N|N|C|C|C|N|N"],
    "hdLastState": ["1"],
    "hdSelectedQuery": ["0"],
    "hdSearchType": ["ADVANCED"],
    "hdIndex": ["0"],
    "hdCriterias": [
        "taxyr|bathrooms|bedrooms|Class|luc|sfla|nbhd|owner|price|salesdate|com_sf|stories|adrstr|style|taxdist|yr_com|yr_buitl"
    ],
    "hdSelectAllChecked": ["false"],
    "sCriteria": ["0"],
    "selSortBy": ["PARID"],
    "selSortDir": [" asc"],
    "hdLink": ["../Datalets/Datalet.aspx?sIndex=0&idx=1"],
}

response = requests.post(
    "https://publicaccess.claytoncountyga.gov/search/advancedsearch.aspx",
    params=params,
    cookies=cookies,
    data=data,
)

print(response)
print(response.text)

assert "LGS HOLDING GROUP 2013 LLC" in response.text
