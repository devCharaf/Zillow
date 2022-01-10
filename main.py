import time
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_driver_path = os.environ['MY_DRIVER']

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22mapBounds%22%3A%7B%22west%22%3A-122.90711440039063%2C%22east%22%3A-121.95954359960938%2C%22south%22" \
             "%3A37.4020368638586%2C%22north%22%3A38.146671071988074%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState" \
             "%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C" \
             "%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value" \
             "%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C" \
             "%22isListVisible%22%3Atrue%7D "
req_headers = {
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': os.environ['MY_USERAGENT'],
}

GOOGLE_DOC_URL = "https://docs.google.com/forms/d/e/1FAIpQLSd4lTiPibnamtjx1MG1k4BNqMkM5otYyUEeGSfL-qWj5JrFFQ/viewform" \
                 "?usp=sf_link "

with requests.Session() as s:
    response = s.get(ZILLOW_URL, headers=req_headers)

# response = requests.get(ZILLOW_URL)
zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, features="html.parser")
list_address = [address.getText() for address in soup.find_all(name="address", class_="list-card-addr")]
list_price = [price.getText() for price in soup.find_all(name="div", class_="list-card-price")]
list_price = [int(price[1:6].replace(",", "")) for price in list_price]
list_link = [link['href'] for link in soup.find_all(name="a", class_="list-card-link list-card-link-top-margin")]

for n in range(len(list_link)):
    if 'https' not in list_link[n]:
        list_link[n] = f'https://www.zillow.com/{list_link[n]}'

# filling the google doc
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(GOOGLE_DOC_URL)


for i in range(len(list_link)):
    question_1 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                                               '1]/div/div[1]/input')
    question_2 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div['
                                               '1]/div/div[1]/input')
    question_3 = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div['
                                               '1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    time.sleep(3)
    question_1.send_keys(list_address[i])
    question_2.send_keys(list_price[i])
    question_3.send_keys(list_link[i])
    submit_button.click()
    submit_another_response = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_response.click()
