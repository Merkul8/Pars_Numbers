import re
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service


link_1 = 'https://hands.ru/company/about'
link_2 = 'https://repetitors.info'

# Данная функция находит номера у многих сайтов, но есть инсключения, тот же link_1.
def find_numbers(url):
    response = requests.get(url)

    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    phone_numbers = re.findall(r'\d{1} \(\d{3}\) \d{3}-\d{2}-\d{2}', str(soup))

    numbers = []

    for phone_number in phone_numbers:
        numbers.append(phone_number)
    
    return numbers

# Эта функция делает поиск номера телефона для первого сайта(link_1), функция ищет всего один номер, и она заточена под один конкретный сайт.
def find_numbers_2(url):
    
    driver = webdriver.Chrome()
    actions = ActionChains(driver)
    
    try:
        driver.maximize_window()
        driver.get(url)
        
        looks_number = driver.find_element(By.CLASS_NAME, 'phone-number__link')
        actions.move_to_element(looks_number).perform()
        looks_number.click()
        
        res_number = driver.find_element(By.ID, 'call-center-phone')
        time.sleep(2)
        
        if res_number.text:
            return res_number.text
        else:
            return 'No phone number found'
        
    except Exception as exc:
        print(exc)
    finally:
        driver.close()
        driver.quit()

# print(find_numbers_2(link_1))
# print(find_numbers_2(link_2))