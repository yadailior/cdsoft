#!/usr/bin/env python
# -*- coding: utf-8 -*-
from googlesearch import search
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import html2text
import ssl
import re


def link_list(code):
    """This function get barcode,
    And search it on google using googlesacrch lib.
     After that store 7 links in list.
    list of links :return """
    links = []
    for link in search(code, tld="co.in", num=5, stop=5, pause=2):
        links.append(link)
    return links


def convert_html_into_text(link):
    """This function get link and send a request to the browser to open the url and read the webpage(as HTML file)
    by using bs4.
    After that make a list of the HTML option tags that in the HTML page.
    After that convert the HTML into text by using html2text lib.
    Return:1)variable that equals to a converted(to text) HTML page
            2)list of tags"""
    req = Request(link, headers={"User-Agent": "Mozilla/5.0"})
    web_page = urlopen(req, context=ssl.SSLContext()).read()
    html_page = BeautifulSoup(web_page, "html.parser")
    option_tag_list = BeautifulSoup(web_page, "html.parser").find_all("option")
    html_text = html2text.html2text(str(html_page))
    return html_text, option_tag_list


def open_and_find(convert_html, tag, code):
    """This function use the variable which return from :"convert_html_into_text" function,
    And open a temporary text file to store the  text from the converted html page-
      to make the search be more comfortable.
      And take the tag list from :"convert_html_into_text" function and convert each tag to text by using html2text lib
    Then by using "for loop", search 3 specifics strings to find the line that contain the "price".
      Return:price line"""

    with open("temp.txt", "w", encoding="utf-8") as temp_text_file:
        temp_text_file.write(convert_html)
        with open("test.txt", "w", encoding="utf-8") as clean_file:
            with open("temp.txt", "r", encoding="utf-8") as lines:
                for line in lines.readlines():
                    if not line.isspace():
                        clean_file.write(line)
    with open("test.txt", "r", encoding="utf-8") as f:
        lines = len(f.readlines())
        f.seek(0)
        counter = 0
        line = f.readline()
        option_list = []
        for option in tag:
            option_list.append(html2text.html2text(str(option)))
        numbers_option = []
        for opt in option_list:
            temp_number = re.findall('[0-9,]+', opt)
            for num in temp_number:
                if "," in num:
                    num = re.sub(',', '', num)
                numbers_option.append(num)
        while code not in line:
            if counter == lines:
                return False
            else:
                line = f.readline()
                counter += 1
        while line.find("₪" or "ILS") < 0:
            if counter >= lines:
                return False
            else:
                line = f.readline()
                counter += 1
        while True:
            if line.find("₪" or "ILS") > 0:
                pass
            else:
                line = f.readline()
                counter += 1
                continue
            if len(tag) == 0:
                if len(re.findall('[0-9,]+', line)) > 0:
                    return line
                else:
                    line = f.readline()
                    counter += 1
                    continue
            if counter >= lines:
                return False
            price=re.findall(r'\d{1,4}(?:[.,]\d{3})*(?:[.,]\d{2})?',line)
            clean_price = {}
            for p in price:
                if len(p) < 3:
                    continue
                if "," in p:
                    clean_price[p]=(re.sub(',', '', p))
                else:
                    clean_price[p]=p
            for price in clean_price:
                if clean_price[price] in numbers_option:
                    line = f.readline()
                    counter += 1
                    break
                else:
                    return clean_price[price]



def numeric_price(line):
    """This function use the variable which return from :"open_and_find" function,
    And store only the numeric character in the price variable using: "for-loop".
     Return: the price variable"""

    if not line:
        price = "Null"
        return price

    price = re.search('[0-9,]+', line).group()
    if "," in price:
        price = re.sub(',', '', price)
    if price.isnumeric():
        return int(price)
    return price
