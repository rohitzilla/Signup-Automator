from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import random
import time
import csv
import calendar

login_page = "https://www.amazon.com/ap/register?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_custrec_newcust"

words = ["first", "last", "name,full", "mail", "user", "month", "day", "year", "age", "country", "state", "phone,number", "zip,post", "job,company", "pass"]
wordpos = {}
info = []
attributes = ["id", "name", "placeholder", "text"]

first_names = []
last_names = []

file = open("users.csv", mode="w")

writer = csv.writer(file, delimiter=",")
writer.writerow(words)

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (content_type is not None and content_type.find('html') > -1)

def readFirstNames():
    global first_names
    input = open("first_names.txt", "r")
    for line in input:
        text = line.split(",")
        first_names.append(text[0])

def readLastNames():
    global last_names
    input = open("last_names.csv", "r")
    for line in input:
        text = line.split(",")
        if text[0] == "name":
            continue
        last_names.append(text[0].lower().capitalize())

def generateRandomInfo():
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$^&"
    first = str(random.choice(first_names))
    last = str(random.choice(last_names))
    full = first + " " + last
    pwd = "".join([random.choice(charset) for i in range(10)])
    user = first + last[0] + str(random.randint(10000, 100000))
    email = user + "@gmail.com"
    day = random.randint(1, 28)
    month = calendar.month_abbr[random.randint(1, 12)]
    year = random.randint(1970, 2001)
    age = 2018 - year
    country = "USA"
    state = "Texas"
    job = "Computer"
    number = random.randint(1000000000, 9999999999)
    zip = random.randint(10000, 99999)
    global info
    info = [first, last, full, email, user, month, day, year, age, country, state, number, zip, job, pwd]

    for i in range(len(words)):
        word = words[i]
        for a in word.split(","):
            wordpos[a] = i
    writer.writerow(info)

def attemptLogon():
    generateRandomInfo()
    driver = webdriver.Firefox()
    driver.get(login_page)
    for word in words:
        for a in word.split(","):
            search(a, driver)

def search(word, driver):
    html = BeautifulSoup(simple_get(login_page), 'html.parser')

    for i in html.findAll(['input', 'select']):
        for att in attributes:
            if word in str(i.get(att)).lower() and not driver.find_element_by_name(i.get("name")).get_attribute("value"):
                if att == "id" and not driver.find_element_by_name(i.get("name")).get_attribute("value"):
                    try:
                        driver.find_element_by_id(i.get(att)).send_keys(info[wordpos[word]])
                        print(info[wordpos[word]])
                    except:
                        pass
                elif att == "name" and not driver.find_element_by_name(i.get("name")).get_attribute("value"):
                    try:
                        driver.find_element_by_name(
                            i.get(att)).send_keys(info[wordpos[word]])
                        print(info[wordpos[word]])
                    except:
                        pass
                elif att == "placeholder" and not driver.find_element_by_name(i.get("name")).get_attribute("value"):
                    try:
                        driver.find_element_by_placeholder(
                            i.get(att)).send_keys(info[wordpos[word]])
                        print(info[wordpos[word]])
                    except:
                        pass
                if word == words[-1]:
                    try:
                        driver.find_element_by_name(
                            i.get("name")).send_keys(Keys.ENTER)
                    except:
                        pass
            elif word in str(i.get(att)).lower() and i.name == 'select':
                if att == "id" and not driver.find_element_by_name(i.get("name")).get_attribute("value"):
                    try:
                        select = Select(driver.find_element_by_id(i.get(att)))
                        select.select_by_visible_text(str(info[wordpos[word]]))
                        print(info[wordpos[word]])
                    except:
                        pass
                elif att == "name" and not driver.find_element_by_name(i.get("name")).get_attribute("value"):
                    try:
                        select = Select(driver.find_element_by_name(i.get(att)))
                        select.select_by_visible_text(str(info[wordpos[word]]))
                        print(info[wordpos[word]])
                    except:
                        pass
                elif att == "placeholder" and not driver.find_element_by_name(i.get("name")).get_attribute("value"):
                    try:
                        select = Select(
                            driver.find_element_by_placeholder(i.get(att)))
                        select.select_by_visible_text(str(info[wordpos[word]]))
                        print(info[wordpos[word]])
                    except:
                        pass
                if word == words[-1]:
                    try:
                        driver.find_element_by_name(
                            i.get("name")).send_keys(Keys.ENTER)
                    except:
                        pass
        if word == words[-1]:
            try:
                driver.find_element_by_name(i.get("name")).send_keys(Keys.ENTER)
            except:
                pass
readFirstNames()
readLastNames()

for i in range(1):
    attemptLogon()
