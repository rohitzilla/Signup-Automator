from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import random
import csv
import calendar
import urllib

login_page = "https://profile.oracle.com/myprofile/account/create-account.jspx" # change this to whatever page you want

words = ["first", "last","user", "name,full", "mail", "month", "day", "year", "age", "country", "state", "city", "address", "phone,number", "zip,post", "job,company", "pass"]
wordpos = {}
info = []
attributes = ["id", "name", "placeholder"]

input_list = []
select_list = []

first_names = []
last_names = []
cities = set()
states = set()

file = open("users.csv", mode="w")

writer = csv.writer(file, delimiter=",")
writer.writerow(words)

# return inputs to fill info into
def getInputs(url):
    html = BeautifulSoup(urllib.request.urlopen(login_page), 'html.parser')
    inputs = html.findAll(['input', 'select'])
    for input in inputs:
        found = False
        for att in attributes:
            for word in words:
                for a in word.split(","):
                    if a in str(input.get(att)).lower() and not found:
                        if input.name == "input" and input.type != "checkbox":
                            input_list.append([att, input.get(att), words.index(word)])
                        elif input.name == "select":
                            select_list.append([att, input.get(att), words.index(word)])
                        found = True

def search(driver):
    for i in range(len(select_list)):
        list = select_list[i]
        if list[0] == "id":
            try:
                select = Select(driver.find_element_by_id(list[1]))
                select.select_by_visible_text(str(info[list[2]]))
                print(info[list[2]])
            except:
                pass
        elif list[0] == "name":
            try:
                select = Select(driver.find_element_by_name(list[1]))
                select.select_by_visible_text(str(info[list[2]]))
                print(info[list[2]])
            except:
                pass
        elif list[0] == "placeholder":
            try:
                select = Select(driver.find_element_by_placeholder(list[1]))
                select.select_by_visible_text(str(info[list[2]]))
                print(info[list[2]])
            except:
                pass
    for i in range(len(input_list)):
        list = input_list[i]
        if list[0] == "id":
            try:
                if "phone" in words[list[2]]:
                    driver.find_element_by_id(list[1]).click()
                driver.find_element_by_id(list[1]).send_keys(info[list[2]])
                print(info[list[2]])
                if words[list[2]] == "pass":
                    driver.find_element_by_id(list[1]).send_keys(Keys.ENTER)
                    print("Enter")
            except:
                pass
        elif list[0] == "name":
            try:
                if "phone" in words[list[2]]:
                    driver.find_element_by_name(list[1]).click()
                driver.find_element_by_name(list[1]).send_keys(info[list[2]])
                print(info[list[2]])
                if words[list[2]] == "pass":
                    driver.find_element_by_name(list[1]).send_keys(Keys.ENTER)
                    print("Enter")
            except:
                pass
        elif list[0] == "placeholder":
            try:
                if "phone" in words[list[2]]:
                    driver.find_element_by_placeholder(list[1]).click()
                driver.find_element_by_placeholder(list[1]).send_keys(info[list[2]])
                print(info[list[2]])
                if words[list[2]] == "pass":
                    driver.find_element_by_placeholder(list[1]).send_keys(Keys.ENTER)
                    print("Enter")
            except:
                pass

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
    info = [first, last, user, full, email, month, day, year, age, country, state, city, address, number, zip, job, pwd]

    for i in range(len(words)):
        word = words[i]
        for a in word.split(","):
            wordpos[a] = i
    writer.writerow(info)

def attemptLogon():
    generateRandomInfo()
    getInputs(login_page)
    driver = webdriver.Firefox()
    driver.get(login_page)
    search(driver)

readFirstNames()
readLastNames()
readCitiesAndStates()
attemptLogon()
