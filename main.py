import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


from requests.api import head

headers = {"Accept-Language" : "en-US, en;q=0.5"} #translate the page into English

url = "YOURWEBSITEHERE" 

results = requests.get(url, headers=headers) # gets the contents of the page by requesting the URL

soup = BeautifulSoup(results.text, "html.parser") #BeautifulSoup specifies the desired format of results using the HTML parser



#the following variables are the types of data we want to extract
variables = []

#each movie div container
names = soup.findAll('TAG', class_='CLASSES') #finds all divs that have the class "xxxxx"


for container in names:
    name = container.h3.a.text #the name of the movie is inside the container > div > h3 > a > NAME (text)
    names.append(name)
    

#dataframe with Pandas to break the data down into a nice table
names = pd.DataFrame({

    'name' : names,

})

#fixing variables and whatnot
names['name'] = names['name'].str.extract('(\d+)').astype(int)



names.to_csv('names.csv')
