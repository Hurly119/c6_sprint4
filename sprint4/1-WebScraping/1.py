from time import sleep
import time
from IPython import embed
import random
import re
import requests

from bs4 import BeautifulSoup
htmls = ["""
<html>
    <head></head>
    <body>
        <div id="target">Hello World</div>
    </body>
</html>
""","""
<html>
    <head></head>
    <body>
        <div>A</div>
        <div>B</div>
        <div>C</div>
        <div>D</div>
    </body>
</html>
""",
"""
<html>
    <head></head>
    <body>
        <a = href="/a.html">A</div>
        <a = href="/b.html">A</div>
        <a = href="/c.html">A</div>
        <a = href="/d.html">A</div>

        <script>
            var hello = "yoh";
            alert(hello);
        </script>
    </body>
</html>
"""]

headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64)"}
time.sleep(2)

BASE_URL = "https://albertyumol.github.io/"
def delay(seconds):
    print(f"Sleeping for {seconds} seconds")
    sleep(seconds)

def get_random_number():
    return random.randint(1,5)

def generate_html(index):
    return htmls[index]

def soup1():
    html_doc = generate_html(0)
    soup = BeautifulSoup(html_doc,"html.parser")
    target = soup.find(id="target")
    print(target.get_text())

def soup2():
    html_doc = generate_html(1)
    soup = BeautifulSoup(html_doc,"html.parser")
    div_elements = soup.find_all('div')
    for div_element in div_elements:
        print(div_element.get_text())

def soup3():
    html_doc = generate_html(2)
    soup = BeautifulSoup(html_doc,"html.parser")
    anchor_elements = soup.find_all('a',href=True)
    for anchor_element in anchor_elements:
        print(anchor_element["href"])

def soup4():
    html_doc = generate_html(2)
    soup = BeautifulSoup(html_doc,"html.parser")
    script_element = soup.find("script", text=re.compile("var hello = \"(.*?)\";")).string
    print(script_element)

def soup5():
    target_page = BASE_URL + "index.html"

    for x in range(1,5):
        if x != 1:
            target_page = BASE_URL + f"page{x}/"+"index.html"
            
        html_content = extract_html_content(target_page)
        soup = BeautifulSoup(html_content,"html.parser")
        elements = soup.find_all("a", {"rel":"permalink"})

        for element in elements:
            print(element.get_text())


def extract_html_content(target_url):
    response = requests.get(target_url,headers)
    return response.text
def main():
    # for x in range(1,5):
    #     print(x)
    #     delay(seconds=get_random_number())
    # a = 5
    # b = 3
    #
    # embed()
    #
    # print(a)
    # print(b)

    soup5()

if __name__ == "__main__":
    main()
