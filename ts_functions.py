import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
from time import sleep

"""Guidelines for this code:
. Use raw string as much as possible
. Group the neccessary data in easy to understand formats or at least name them similarly
. Aways have a copy in another file when you are going to make a big change
. Remember the philosophy of 1 = PNH + PH and that way to solve hard problems, time is gold
"""

keys = ['age', 'numeration', 'popularity', 'country', 'num_of_comments', 'time', 'sex', 'text', 'temporales']

# Getting started(Pass another url if you don't want the default starter):
def start_selenium(url=r'https://tusecreto.io/#/recent'):
    # Chrome driver path
    chrome_path = r'C:\Program Files\chromedriver.exe'
    # Selenium "getting into the page" or setup
    ser = Service(chrome_path)
    driver = webdriver.Chrome(service=ser)
    driver.get(url)
    driver.implicitly_wait(5)
    return driver


def get_secrets(driver):
    # Getting the "passive data":
    # We get almost everything from just secret.text
    all_secrets_info = []
    secrets = driver.find_elements(By.CSS_SELECTOR, 'div.secret')
    for secret in secrets:
        s_list = secret.text.split('\n')
        # All 8 pieces of data
        age = s_list[0]
        numeration = s_list[1]
        popularity = s_list[2]
        country = s_list[4]
        text = s_list[5]
        num_of_comments = [6]
        time = secret.find_element(By.CSS_SELECTOR, '.timeago').get_attribute('title')
        sex = secret.get_attribute('class')
        # TODO -> Identify and classify special text
        if sex == 'secret  secret-0 ':
            sex = 'Anonymous'
        elif sex == 'secret  secret-1 ':
            sex = 'Man'
        elif sex == 'secret  secret-2 ':
            sex = 'Woman'
        secret_info = {'age': age, 'numeration': numeration, 'popularity': popularity, 'country': country, 'num_of_comments': num_of_comments, 'time': time, 'sex': sex, 'text': text}
        all_secrets_info.append(secret_info)
    return all_secrets_info


# All af these grab functions can be better suited for manual revision because there probably aren't many :p and the systems are never 100% accurate


def grab_temporales(text):
    # grab any http and then work to chip the stone  -> delete any non formatted characters
    print("\n")
    raw_possible_codes = re.findall(r'\b\w{6}\b', text)
    print(raw_possible_codes)
    for raw_possible_code in raw_possible_codes:
        if raw_possible_code is not None:
            raw_possible_code = raw_possible_code
            possible_code = ''
            for char in raw_possible_code:
                if char.isalnum():
                    possible_code += char
            try:
                print(r'https://www.imagenes-temporales.com/subidas/ver/' + possible_code)
                url = urlopen(r'https://www.imagenes-temporales.com/subidas/ver/' + possible_code).read()
                soup = BeautifulSoup(url, 'html.parser')
                # One type of page has sth the other doesn't
                print(soup.body)
                if soup.body.find(string=re.compile(r'Subida por .*')):
                    driver = start_selenium(r'https://www.imagenes-temporales.com/subidas/ver/' + possible_code)
                    sleep(3.5)
                    html = driver.find_element(By.TAG_NAME, 'html')
                    html.send_keys(Keys.END)
                    driver.save_screenshot(r'C:\Users\odeig\Desktop\Python Skills\TS\images\\' + possible_code + '.png')
                print(r'https://www.imagenes-temporales.com/subidas/ver/' + possible_code)
                return possible_code
            except HTTPError:
                pass
            except UnicodeEncodeError:
                pass


def grab_phones(text):
    # If has + and more than 7 numbers(8)
    digits = '+'
    for character in text:
        if character.isdigit():
            digits += character
    if digits > 8 and '+' in text:
        return digits
    else:
        return None
    

def check_for_url(text):
    # Check for the http keyword and return True if it has it, another function may be better suited for advanced settings
    if ['http', 'htt', 'ttp'] in text:
        return True
    else:
        return None



def get_popular_messages(popularity):
    # Gets all the messages that have more or the same amount of likes as X
    chosen_ones = []
    write_to_file = input("Write to fiel? (Y/N)")
    with open('secrets.csv', 'r', encoding='utf-8', newline='') as secrets:
        reader = csv.DictReader(secrets, fieldnames=keys)
        if popularity >= 0:
            if write_to_file == 'Y':
                with open('temporal.csv', 'w', encoding='utf-8', newline='') as chosen_ones:
                    writer = csv.DictWriter(chosen_ones, fieldnames=keys)
                    for row in reader:
                        if int(row['popularity']) >= popularity:
                            writer.writerow(row)
            else:
                for row in reader:
                        if int(row['popularity']) >= popularity:
                            print(row)
        else:
            if write_to_file == 'Y':
                with open('temporal.csv', 'w', newline='') as chosen_ones:
                    writer = csv.writer(chosen_ones)
                    for row in reader:
                        if int(row['popularity']) <= popularity:
                            writer.writerow(row)

            else:
                for row in reader:
                    if int(row['popularity']) <= popularity:
                        print(row)



def get_commented_messages(comments, number_of_mssgs=-1):
    # Gets a certain amount of messages(default is all the messages) with a popularity higuer or equal to X(if X is - then we return the unpopular messages)

    pass