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
chromeOptions.add_argument("--user-data-dir=/home/root/.config/google-chrome/Default")
chromeOptions.add_argument("--headless")
service = Service(executable_path="./chromedriver")
browser = webdriver.Chrome(service=service, options=chromeOptions)

def initBrowser():
    browser.get("https://www.instagram.com/?hl=fr")
    print("1 - Page Opened")
    print(datetime.now())
    sleep(5)

def wait():
    sleep(random.randint(4,7))

def fetchOldestPendingMessageFromDB():
    # Call API with params : status = 0, sort = ASC, limit = 1
    fetchedMessage = requests.get("https://la-boite-a-message-v2-api.herokuapp.com/messages?_where[status]=0&_sort=created_at:ASC&_limit=1").json()
    # Check if fetchedMessage empty or not
    if fetchedMessage:
        # Return formated message with only usefull datas
        return [fetchedMessage[0]['id'],fetchedMessage[0]['target'],fetchedMessage[0]['message'],fetchedMessage[0]['social']]
    else:
        return None
def getBotStatus():
    status = requests.get("https://la-boite-a-message-v2-api.herokuapp.com/infos?info=bot_status&_limit=1").json()
    return status[0]['status']

def change_status(id):
    # Change desired message status to '1' meaning sent
    requests.put(f"https://la-boite-a-message-v2-api.herokuapp.com/messages/{id}",
    data=json.dumps({
    'status': [1]
    }),
    headers={
    'Content-Type': 'application/json'
    })
    print('status_changed')   

def change_status_error(id):
    # Change desired message status to '2' meaning error (emojis)
    requests.put(f"https://la-boite-a-message.herokuapp.com/messages/{id}",
    data=json.dumps({
    'status': [2]
    }),
    headers={
    'Content-Type': 'application/json'
    })
    print('status_changed_err')
    
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', string)

def process_img(user):
    img = Image.open(f"./data/image/letter.png")
    W = 1000
    if len(user)<=12:
        size = 100
    elif len(user)>12:
        size = int(100 - 3*(int(len(user)-12)))

    font = ImageFont.truetype(f"./data/font/helvetica.ttf",size)
    process = ImageDraw.Draw(img)
    w, h = process.textsize(user,font=font)
    process.text(((W-w)/2,390),user,(120,120,120),font = font)
    process.text(((W-w)/2,385),user,(250,250,250),font = font)
    img.save(f"./data/image/upload.png")


def post_message(id,user,msg):
    try:
        msg = remove_emoji(msg)
        print("Processing post")
        process_img(user)
        try:
            browser.get("https://www.instagram.com/")
            sleep(10)
        except:
            print('Error - get instagram')
        try:
            browser.execute_script('document.getElementsByTagName("button")[document.getElementsByTagName("button").length-1].click()')
            sleep(5)
        except:
            print('Error - new post')
           
        try:
            browser.execute_script("select = document.getElementsByTagName('input')[3];")
            sleep(1)
        except:
            print('Error - find to classname')
           
        try:
            browser.execute_script("select.classList = 'selected';")
            sleep(2)
        except:
            print('Error - add class')
           
        try:
            browser.find_element(By.CLASS_NAME, "selected").send_keys(os.path.abspath("/root/laboiteamessage/data/image/upload.png"))
            print('- Image sent')
            wait()
        except:
            print('Error - Send image input')
           
        try:
            browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[1]/div/div/div[3]/div/button').click()
            print('- Skip')
            wait()
        except:
            print('Error - 1st skip')
           
        try:
            browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[1]/div/div/div[3]/div/button').click()
            print('- Skip')
            wait()
        except:
            print('Error - 2nd skip')
           
        try:
            browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea").send_keys(f"@{user} : {msg}")
            print('- Text set')
            wait()
        except:
            print(f"Error - bad message")
            change_status_error(id)
            return
        try:
            browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[1]/div/div/div[3]/div/button').click()
            print('- Done')
            change_status(id)
        except:
            print('Error - post')
           
    except Exception as e:
        print(f"[ERROR] {e}")
def stopBot():
    while True:
        print('stopped')
        status = getBotStatus()
        if status != '2':
            break
        sleep(60)
initBrowser()
while True:
    select_msg = fetchOldestPendingMessageFromDB()
    print(select_msg)
    if select_msg == None:
        print("continue")
        sleep(60)
        continue
    if select_msg[3] == 0:
        # Process image
        process_img(select_msg[1])
        # Post      |    ID    |     |   TARGET  |    |  MESSAGE  |
        post_message(select_msg[0],select_msg[1],select_msg[2])
        
    status = getBotStatus()
    print(status)
    if status == '0':
        print('Normal mode - 5mn')
        sleep(300)
    elif status == '1':
        print('Slow mode - 10mn')
        sleep(600)
    elif status == '2':
        stopBot()
    elif status == '3':
        print('Testing - 5mn')
        sleep(300)
    else:
        print('error')
        sleep(60)
    
    
