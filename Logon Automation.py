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
import urllib

login_page = "https://profile.oracle.com/myprofile/account/create-account.jspx"

words = ["first", "last", "name,full", "mail", "user", "month", "day", "year", "age", "country", "state", "city", "address", "phone,number", "zip,post", "job,company", "pass"]
wordpos = {}
info = []
attributes = ["id", "name", "placeholder", "text"]

first_names = []
last_names = []
cities = set()
states = set()

file = open("users.csv", mode="w")

writer = csv.writer(file, delimiter=",")
writer.writerow(words)

def readFirstNames():
    global first_names
    input = open("first_names.txt", "r")
    for line in input:
        text = line.split(",")
        first_names.append(text[0])

def readCitiesAndStates():
    global cities
    input = open("cities.csv", "r")
    for line in input:
        text = line.split(",")
        if text[0] == "City":
            continue
        cities.add(text[0])
        try:
            states.add(text[2])
        except:
            pass

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
    pwd = "".join([random.choice(charset) for i in range(15)])
    user = first + last[0] + str(random.randint(10000, 100000))
    email = user + "@gmail.com"
    day = random.randint(1, 28)
    month = calendar.month_abbr[random.randint(1, 12)]
    year = random.randint(1970, 2001)
    age = 2018 - year
    country = "USA"
    job = "Computer"
    number = random.randint(1000000000, 9999999999)
    state = random.choice(list(states))
    city = random.choice(list(cities))
    roads = ["Street", "Road", "Lane", "Place"]
    address = str(random.randint(100, 999)) + " " + random.choice(list(cities)) + " " + random.choice(roads)
    zip = random.randint(10000, 99999)
    global info
    info = [first, last, full, email, user, month, day, year, age, country, state, city, address, number, zip, job, pwd]

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
    html = BeautifulSoup(urllib.request.urlopen(login_page), 'html.parser')

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
readCitiesAndStates()
attemptLogon()
