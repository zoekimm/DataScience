#Crawl youtube video links for TV shows based on the query 
#Selenium and Beautiful Soap 

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import requests
import csv
import pandas as pd
from tqdm import tqdm
import time

def isValid(i):
    title = i['title']
    label = i['aria-label']
    publisher = (label.split("by ",1)[1]).split(" ")[0]
    link = 'https://www.youtube.com' + i['href']
    
    check if the publisher of the video is the same as the broadcasting companies
    if company in publisher and all(x not in title for x in excluded):
        csvWriter.writerow([TVtitle, company, title, publisher, link])

def link():
    search = (TVtitle + ' ' + company).replace(' ', '+')
    PATH = r'/Applications/chromedriver'
    driver = webdriver.Chrome(PATH)
    driver.get(f'https://www.youtube.com/results?search_query={search}')
    body = driver.find_element_by_tag_name('body')
    
    pageDown = 15 #Can change the number of scrolling down
    while pageDown != 0:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        pageDown = pageDown - 1

    source = driver.page_source
    soup = BeautifulSoup(source, 'lxml')
    videohtml = soup.find_all('a', {'id' :'video-title'})

    for i in tqdm(videohtml, total=len(videohtml)):
        isValid(i)

    driver.close()

#Csv file ['TVtitle', 'Company', 'YoutubeTitle', 'YoutubePublisher', 'YoutubeLink']
csvFile = open('youtube_crawl.csv', 'w')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(['TVtitle', 'Company', 'YoutubeTitle', 'YoutubePublisher', 'YoutubeLink'])

excluded = ['대상', '수상', 'Award', '시상', '콘서트'] #List of words excluded for the data collection

#Load the csv file
df = pd.read_csv('./YoutubeTVShowList.csv')

for index, row in df.iterrows():
    TVtitle = row['원제']
    company = row['채널']
    link() 
