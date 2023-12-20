from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import lxml
import requests
import time
import os

def fetch_detials():
    response = requests.get(url=os.environ['URL'])
    print(response.status_code)

    data = response.text

    soup = BeautifulSoup(data , 'lxml')

    property_links = [ link.get('href') for link in soup.find_all('a' , class_='property-card-link') ]
    prices_list = [ (item.text)[0:6] for item in soup.find_all('span' , class_ = 'PropertyCardWrapper__StyledPriceLine') ]
    address_list = [(item.text).replace('\n' , '').strip().replace('|' , '') for item in soup.find_all('address')]

    return [property_links , prices_list , address_list]


#SELENIUM PART  -> fill hte form automatically

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://docs.google.com/forms/d/e/1FAIpQLSfUR_DLa7GI_F_eCq5NXvtsylm-U9OSqHhlfi48HwnljieY1Q/viewform?usp=sf_link')


def fill_form(price , address , link):
    time.sleep(2)
    house_price_input = driver.find_element(By.XPATH ,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    house_address_input = driver.find_element(By.XPATH , '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    house_link_input = driver.find_element(By.XPATH , '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_btn = driver.find_element(By.XPATH , '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    house_price_input.send_keys(price)
    house_address_input.send_keys(address)
    house_link_input.send_keys(link)
    submit_btn.click()
    time.sleep(1)
    submit_another_respnse = driver.find_element(By.XPATH , '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_respnse.click()

property_details = fetch_detials()

property_links = property_details[0]
prices_list = property_details[1]
address_list = property_details[2]

# We will gather 10 responses
for i in range(10):
    price = prices_list[i]
    address = address_list[i]
    link = property_links[i]
    fill_form(price , address , link)

driver.quit()







