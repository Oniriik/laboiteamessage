import os
import re
import json
import requests
import random
from datetime import *
from time import sleep
from PIL import Image, ImageFont, ImageDraw
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


chromeOptions = Options()
chromeOptions.headless = False
chromeOptions.add_argument("--disable-dev-shm-usage")
chromeOptions.add_argument("--no-sandbox")
chromeOptions.add_argument("--user-data-dir=/home/oniriik/.config/google-chrome/Default")
chromeOptions.add_argument("--headless")
service = Service(executable_path="./chromedriver")
browser = webdriver.Chrome(service=service, options=chromeOptions)

def initBrowser():
    browser.get("https://www.instagram.com/?hl=fr")
    print("1 - Page Opened")
    print(datetime.now())
    sleep(5)

def login():
    sleep(5)
    try:
        browser.find_element(By.XPATH,'/html/body/div[4]/div/div/button[2]').click()
        print('1/6 - Cookies accepted')
        except:
        print('error - Cookies')
    sleep(5)
    try:
        browser.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input').send_keys('laboiteamessage')
        print('2/6 - User input')
    except:
        print('error - User input')
    sleep(5)
    try:
        browser.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input').send_keys('Hemiazqsd!!592447')
        print('3/6 - Password input')
    except:
        print('error - Password input')
    sleep(5)
    try:
        browser.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]/button').click()
        print('4/6 - Log in')
    except:
        print('error - Log in')
    sleep(10)
    try:
        browser.find_element(By.XPATH,'/html/body/div[1]/section/main/div/div/div/div/button').click()
        print('5/6 - Pass auth')
    except:
        print('error - Pass auth')
    sleep(10)
    try:
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[2]').click()
    except:
        print('error - Deny notification')
    print('6/6 - Deny notification')
    sleep(5)
    print('logged')
    sleep(5)
    browser.quit()
initBrowser()
login()