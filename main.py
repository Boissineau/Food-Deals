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
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import process_time


start = time.perf_counter()


# url's of pages to scrape from
base_url = "https://www.tesco.com"
url = "https://www.tesco.com/groceries/en-GB/search?query=bread&icid=tescohp_sws-1_m-ft_in-bread_ab-226-b_out-bread"


# intanitating browsers to use for scraping
browser_options = Options()
browser_options.add_argument("--headless")
browser_options.add_argument("--no-sandbox")
browser_options.add_argument("--incognito")
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
browser_options.add_argument("user-agent={0}".format(user_agent))
# adding a user_agent gets passed the --headless access denied

# intial scrapes
browser = webdriver.Chrome(options=browser_options)
browser.get(url)
soup = BeautifulSoup(browser.page_source, features="lxml")

# soup_log = open('soup_log.txt', 'w')
# print(soup.prettify(), file = soup_log)

# tags your scraper wants to look for
food_div = soup.find_all("div", class_="tile-content")
pagination_a = soup.find("a", attrs={"name": "go-to-results-page"})


# variables
names = []
prices = []


# log for checking w/e
log = open("log.txt", "w", encoding="utf-8")


# continues to search till no more next pages
while True:
    # print(len(names))
    # searches through each container/div/tag/whatever it is
    for container in food_div:
        name = container.h3.a.text
        names.append(name)
        print(name + "\n", file=log)
    try:
        a = pagination_a["href"]
    except:
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
