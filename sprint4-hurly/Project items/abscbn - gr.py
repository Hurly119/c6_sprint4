import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PATH = 'C:\Program Files\chromedriver.exe'
driver = webdriver.Chrome(PATH)


driver.get("https://news.abs-cbn.com/special-pages/search?q=vaccination#gsc.tab=0&gsc.q=vaccination&gsc.page=1")

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
            print(f'Page: {page}')
            print(link)


get_urls(1)

# PAGE 2 ONWARDS
for p in range(1, totalpages+1):
    driver.maximize_window()
    # driver.execute_script('window.scrollBy(0, 1000)', '')

#     pbutton = driver.find_element(By.XPATH, '//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div[1]/div/div[2]/div/div[2]')
    page = p+1
    if page > 1:
        # driver.execute_script('window.scrollBy(0, document.body.scrollHeight)', '')
        # wait = WebDriverWait(driver, 10)
        # wait.until(EC.element_to_be_clickable(
        #    (By.XPATH, '//*[@id="___gcse_0"]/div/div/div/div[5]/div[2]/div[1]/div/div[2]/div/div[2]'))).click()
        #         pbutton.click()
        url = "https://news.abs-cbn.com/special-pages/search?q=vaccination#gsc.tab=0&gsc.q=vaccination&gsc.page=%s" % page
        driver.get(url)
        get_urls(page)
        time.sleep(15)


time.sleep(15)

driver.quit()
# %% codecell

df = pd.DataFrame({"title": urls.keys(), "link": urls.values()})
# %% codecell

df.to_csv("abscbn_headlines.csv")
