from os import link
import lxml
from pandas.core.arrays.categorical import contains
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from requests.api import head
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import process_time
from tescoList import Tesco
from nameList import foodNames


start = time.perf_counter()


# url's of pages to scrape from
Count = 0
base_url = "https://www.tesco.com"

browser_options = Options()
browser_options.add_argument("--headless")
browser_options.add_argument("--no-sandbox")
browser_options.add_argument("--incognito")
browser_options.add_argument("--disable-gpu")
browser_options.add_argument("--disable-extensions")
browser_options.add_argument("--no-proxy-server")
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
browser_options.add_argument("user-agent={0}".format(user_agent))

browser = webdriver.Chrome(options=browser_options)
browser2 = webdriver.Chrome(options=browser_options)


while Count < len(Tesco):
    url = Tesco[Count]
    url2 = "https://groceries.morrisons.com/search?entry=bread"

    # intanitating browsers to use for scraping
    # adding a user_agent gets passed the --headless access denied

    # intial scrapes
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, features="lxml")
    browser2.get(url2)
    soup2 = BeautifulSoup(browser2.page_source, features="lxml")

    soup_log = open('logging/soup_log.txt', 'w')
    print(soup2.prettify(), file = soup_log)

    # tags your scraper wants to look for. I.E. The cotainer element, not the specific element. (The container surrounding the item not the specific price, name, link, etc...)
    food_div = soup.find_all("div", class_="tile-content")
    pagination_a = soup.find("a", attrs={"name": "go-to-results-page"})
    food_div2 = soup2.find_all("li", class_="fops-item fops-item--cluster")





    # variables
    names = []
    prices = []
    redirects = []

    names2 = []


    # log for checking w/e
    log1 = open("logging/names.txt", "w", encoding="utf-8")
    log2 = open("logging/prices.txt", "w", encoding="utf-8")
    log3 = open("logging/redirects.txt", "w", encoding="utf-8")


    # continues to search till no more next pages
    while True:
        # print(len(names))
        # searches through each container/div/tag/whatever it is
        for container in food_div:
            name = container.h3.a.text
            names.append(name)
            price = container.find('span', class_='value').text if container.find('span', class_='value') is not None else ''
            prices.append(price)
            href = container.h3.a['href'] if container.h3.a['href'] is not None else ''
            redirects.append(base_url + href)
            # print(name + "\n", file=log1)
            # print(price + "\n", file=log2)
            # print(href + "\n", file=log3)

        for container in food_div2:
            name = container.find('h4', class_='fop-title')['title']    if container.find('h4', class_='fop-title') is not None else ''
            # name = container.find('div', class_='fop-description').h4.span.text
            # description = container.find('div', class_='fop-description')
            names2.append(name)


    
        # end of next pages
        try:
            a = pagination_a['href']
        except:
            print(pagination_a)
            Count = Count + 1
            break



        # gets next page 
        new_url = pagination_a["href"]
        if new_url is None:
            break
        url = base_url + new_url
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, features="lxml")
        food_div = soup.find_all("div", class_="tile-content")
        pagination_a = soup.find("a", attrs={"name": "go-to-results-page"})

    stop = time.perf_counter()
    print(stop - start)
   

