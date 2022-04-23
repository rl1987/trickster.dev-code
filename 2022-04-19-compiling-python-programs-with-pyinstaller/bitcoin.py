#!/usr/bin/python3

from tkinter import *
from datetime import datetime

import requests
from lxml import html

previous = None

# Grab the bitcoin price
def Update():
    global previous

    resp = requests.get("https://www.coindesk.com/price/bitcoin")
    print(resp.url)

    tree = html.fromstring(resp.text)
    price_large = tree.xpath('//span[contains(@class, "briNjb")]')[0].text
    price_large = price_large.replace(",", "")

    print(price_large)

    # Update our bitcoin label
    bit_label.config(text=price_large)
    # Set timer to 30 seconds
    # 1 second = 1000
    root.after(30000, Update)

    # Get Current Time
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")

    # Update the status bar
    status_bar.config(text=f"Last Updated: {current_time}   ")

    # Determine Price Change
    # grab current Price
    current = price_large

    # remove the comma
    current = current.replace(",", "")

    if previous is not None:
        if float(previous) > float(current):
            latest_price.config(
                text=f"Price Down {round(float(previous)-float(current), 2)}", fg="red"
            )

        elif float(previous) == float(current):
            latest_price.config(text="Price Unchanged", fg="grey")

        else:
            latest_price.config(
                text=f"Price Up {round(float(current)-float(previous), 2)}", fg="green"
            )
    else:
        previous = current
        latest_price.config(text="Price Unchanged", fg="grey")


def main():
    global root
    global bit_label
    global status_bar
    global previous
    global latest_price

    root = Tk()
    root.title("Bitcoin Price Grabber")
    root.geometry("550x210")
    root.config(bg="black")

    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")

    my_frame = Frame(root, bg="black")
    my_frame.pack(pady=20)

    logo = PhotoImage(file="images/bitcoin.png")
    logo_label = Label(my_frame, image=logo, bd=0)
    logo_label.grid(row=0, column=0, rowspan=2)

    bit_label = Label(
        my_frame, text="TEST", font=("Helvetica", 45), bg="black", fg="green", bd=0
    )
    bit_label.grid(row=0, column=1, padx=20, sticky="s")

    latest_price = Label(
        my_frame, text="move test", font=("Helvetica", 8), bg="black", fg="grey"
    )
    latest_price.grid(row=1, column=1, sticky="n")

    # Create status bar
    status_bar = Label(
        root,
        text=f"Last Updated {current_time}   ",
        bd=0,
        anchor=E,
        bg="black",
        fg="grey",
    )

    status_bar.pack(fill=X, side=BOTTOM, ipady=2)

    # On program start, run update function
    Update()

    root.mainloop()


if __name__ == "__main__":
    main()
