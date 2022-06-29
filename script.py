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

service = Service(executable_path="./chromedriver")
browser = webdriver.Chrome(service=service, options=chromeOptions)

def initBrowser():
    browser.get("https://www.instagram.com/?hl=fr")
    print("1 - Page Opened")
    print(datetime.now())
    sleep(5)

def wait():
    sleep(random.randint(3,5))

def fetchOldestPendingMessageFromDB():
    # Call API with params : status = 0, sort = ASC, limit = 1
    fetchedMessage = requests.get("https://la-boite-a-message-v2-api.herokuapp.com/messages?_where[status]=0&_sort=created_at:ASC&_limit=1").json()
    # Check if fetchedMessage empty or not
    if fetchedMessage:
        # Return formated message with only usefull datas
        return [fetchedMessage[0]['id'],fetchedMessage[0]['target'],fetchedMessage[0]['message'],fetchedMessage[0]['social']]
    else:
        return None

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
        browser.get("https://www.instagram.com/")
        sleep(10)
        browser.execute_script('document.getElementsByTagName("button")[document.getElementsByTagName("button").length-1].click()')
        wait()
        browser.execute_script("select = document.getElementsByTagName('input')[3];")
        browser.execute_script("select.classList = 'selected';")
        sleep(2)
        browser.find_element(By.CLASS_NAME, "selected").send_keys(os.path.abspath("./data/image/upload.png"))
        print('- Image sent')
        wait()
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[1]/div/div/div[3]/div/button').click()
        print('- Skip')
        wait()
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[1]/div/div/div[3]/div/button').click()
        print('- Skip')
        wait()
        try:
            browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea").send_keys(f"@{user} : {msg}")
            print('- Text set')
        except Exception as e:
            print(f"[ERROR] {e}")
            change_status_error(id)
            return
        wait()
        browser.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/div/div/div/div[1]/div/div/div[3]/div/button').click()
        print('- Done')
        change_status(id)
    except Exception as e:
        print(f"[ERROR] {e}")



# initBrowser()
# post_message('1585','tim','test')


change_status(16)
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
    sleep(120)
    