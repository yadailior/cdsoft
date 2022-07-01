#!/usr/bin/env python
# -*- coding: utf-8 -*-
from moduls import function as func

barcode = input("Please insert barcode for search on google :")

prices_list = []

website_price = {}

links = func.link_list(barcode)

for link in links:
    con_html, otl = func.convert_html_into_text(link)

    price_line = func.open_and_find(con_html, otl, barcode)

    price = (func.numeric_price(price_line))

    website_price[link] = price

    if type(price) == int:
        prices_list.append(price)

lowest_price = min(prices_list)

for k, v in website_price.items():
    if v == lowest_price:
        print("The lowest price")
        print("-" * 80)
        print(f"url:{k}", f"price:{v}")
        print("-" * 80)
    else:
        print(f"url:{k}", f"price:{v}")
