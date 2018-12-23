from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import random
import time
import csv

login_page = "https://www.walmart.com/account/signup"

words = ["first", "last", "name", "mail", "user", "pass"]
info = []
attributes = ["id", "name", "placeholder", "text"]

first_names = []
last_names = []

file = open("users.csv", mode="w")

writer = csv.writer(file, delimiter=",")
writer.writerow(words)

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
    charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    first = str(random.choice(first_names))
    last = str(random.choice(last_names))
    full = first + " " + last
    pwd = "".join([random.choice(charset) for i in range(10)])
    user = first + last[0] + str(random.randint(10000, 100000))
    email = user + "@gmail.com"
    global info
    info = [first, last, full, email, user, pwd]

    writer.writerow(info)

def attemptLogon():
    generateRandomInfo()
    driver = webdriver.Firefox()
    driver.get(login_page)
    for word in words:
        search(word, driver)
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.current_url != login_page)
    driver.close()

def search(word, driver):
    for att in attributes:
        for elem in driver.find_elements_by_xpath("//*[@{0}]".format(att)):
            if word in elem.get_attribute(att).lower() and elem.tag_name == "input":
                if att == "id" and word != "sign" and not elem.get_attribute("value"):
                    try:
                        driver.find_element_by_id(elem.get_attribute(
                            att)).send_keys(info[words.index(word)])
                        print(info[words.index(word)])
                    except:
                        pass
                elif att == "name" and word != "sign" and not elem.get_attribute("value"):
                    try:
                        driver.find_element_by_name(elem.get_attribute(
                            att)).send_keys(info[words.index(word)])
                        print(info[words.index(word)])
                    except:
                        pass
                elif att == "placeholder" and word != "sign" and not elem.get_attribute("value"):
                    try:
                        driver.find_element_by_placeholder(elem.get_attribute(
                            att)).send_keys(info[words.index(word)])
                        print(info[words.index(word)])
                    except:
                        pass
                if word == words[-1]:
                    try:
                        elem.send_keys(Keys.ENTER)
                    except:
                        pass
    if word == words[-1]:
        try:
            elem.send_keys(Keys.ENTER)
        except:
            pass
        return

readFirstNames()
readLastNames()

for i in range(3):
    attemptLogon()
