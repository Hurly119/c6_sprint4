import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

PATH = 'C:\Program Files\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get("https://www.sunstar.com.ph/search")
search = driver.find_element(By.XPATH, '//*[@id="gsc-i-id1"]')
search.send_keys('vaccine')
search.send_keys(Keys.RETURN)

pages = driver.find_elements(By.CSS_SELECTOR, 'div.gsc-cursor-page')
totalpages = len(pages)

urls = dict()


def get_urls(page):
    alinks = driver.find_elements(By.TAG_NAME, "a.gs-title")
    for a in alinks:
        link = a.get_attribute('href')
        title = a.get_attribute("innerHTML").replace("<b>", "").replace("</b>", "")
        if (link != None) and (link not in urls):
            urls[title] = link


get_urls(1)


# PAGE 2 ONWARDS
for p in range(1, totalpages):
    driver.maximize_window()
    driver.execute_script('window.scrollBy(0, 1000)', '')
    page = p+1
    if page > 1:
        driver.execute_script('window.scrollBy(0, document.body.scrollHeight)', '')
        pbutton = '//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div[1]/div/div[2]/div/div[%s]' % page
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, pbutton))).click()
        #         pbutton.click()
        get_urls(page)
        time.sleep(15)


time.sleep(15)

driver.quit()

df = pd.DataFrame({"title": urls.keys(), "link": urls.values()})

df['newsagency'] = 'sunstar'


df.to_csv("sunstar_headlines.csv")


date = []
paragraph = []
for news in df['link']:
    source = requests.get(news, headers={
                          'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}).text
    soup = BeautifulSoup(source, 'html.parser')
    article_date = soup.find('div', attrs={'class': 'articleDate'}).get_text().replace('\n', '')
    block = soup.find_all('div', attrs={'class': 'articleBody articleContent'})
    string = str(block).replace('\r', '').replace('\n', '').replace('\t', '').replace('<br/', '')
    string = string.split('>')
    string = string[2]
    first_paragraph = block.find('p').get_text()
    date.append(article_date)
    first_paragraph = string
    time.sleep(15)


df['date'] = date
df['paragraph'] = paragraph

df.to_csv("sunstar_headlines.csv")

'''
# For testing purposes
blink = 'https://www.sunstar.com.ph/article/1883104/Manila/Local-News/Governors-seek-to-negotiate-directly-with-vaccine-makers'
source = requests.get(blink, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}).text
soup = BeautifulSoup(source, 'html.parser')
article_date = soup.find('div', attrs={'class': 'articleDate'}).get_text().replace('\n', '')
article_date
block = soup.find_all('div', attrs={'class': 'articleBody articleContent'})
string = str(block).replace('\r', '').replace('\n', '').replace('\t', '').replace('<br/', '')
string = string.split('>')
string = string[2]
print(string)
first_paragraph = string
first_paragraph
'''
