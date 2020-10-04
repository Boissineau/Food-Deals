from os import link
from typing import final
from bs4 import element
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
from selenium.webdriver import ChromeOptions, FirefoxOptions
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import process_time, sleep
from tescoList import Tesco
from nameList import foodNames
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start = time.perf_counter()


# url's of pages to scrape from
Count = 0
base_url = "https://www.tesco.com"

browser_options = FirefoxOptions()
# browser_options.add_argument("--headless")
browser_options.add_argument("--incognito")
browser_options.add_argument("--disable-gpu")
browser_options.add_argument("--disable-extensions")
browser_options.add_argument("--no-proxy-server")
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
browser_options.add_argument("user-agent={0}".format(user_agent))


browser2 = webdriver.Firefox(firefox_options=browser_options)


while Count < len(Tesco):
    url = Tesco[Count]
    url2 = "https://groceries.morrisons.com/search?entry=bread"

    browser2.get(url2)
    sleep(10)
    innerHTML = browser2.execute_script("return document.body.innerHTML")
    morrisons_innerHtml = open('logging/morrisons_innerHtml.txt', 'w', encoding='utf-8')

    soup2 = BeautifulSoup(innerHTML, "lxml")
    print(soup2.prettify(), file=morrisons_innerHtml)


    food_div2 = soup2.find_all("li", class_="fops-item--cluster")

    # variables
    names = []
    prices = []
    redirects = []

    names2 = []


    # log for checking w/e

    morrisons_log = open('logging/morrisons_log.txt', 'w', encoding='utf-8')

    # continues to search till no more next pages
    try: 
        while True:


            for container in food_div2:
                name = container.find('h4', class_='fop-title')['title']    if container.find('h4', class_='fop-title') is not None else ''
                # description = container.find('div', class_='fop-description')
                names2.append(name)
                morrisons_log = open('logging/morrisons_log.txt', 'w')

            stop = time.perf_counter()
            print(stop - start)
            print(names2, file=morrisons_log)
            break
    except: 
        browser2.close()


    browser2.close()
    break
