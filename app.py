# Fetch current directory 
import os
from PIL.Image import init
from requests import api
cwd = "/app"

# Imports
try:
    import re
    import json
    import random
    import tweepy
    from datetime import *
    import requests
    from time import sleep
    from data.imports import infos
    from selenium import webdriver
    from PIL import Image,ImageFont,ImageDraw
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options

# If any of imports are unavailable then :     
except Exception as e:
    print(f"#######################\n\n[MODULE MISSING] : {e} ")
    print('\n[Installing modules]\n')
    try:
        # Install missing module
        os.system(f'pip install -r {cwd}/processScript/data/requirement.txt')
    except Exception as e:
        print(f"[ERROR] : {e}")


# Variables
db = infos.db
browser = None

# Local / Server mode
local = False

# Init Twitter API
auth = tweepy.OAuthHandler(infos.consumer_key, infos.consumer_secret)
auth.set_access_token(infos.access_token, infos.access_token_secret)
API = tweepy.API(auth)

# Init Selenium
def initSelenium():
    global browser
    if local ==True:
        chromeOptions = Options()
        chromeOptions.headless = False
        chromeOptions.add_argument("--disable-dev-shm-usage")
        chromeOptions.add_argument("--no-sandbox")
        browser = webdriver.Chrome(f"{cwd}/processScript/data/local/chromedriver",options=chromeOptions)
    else:
        chromeOptions = Options()
        chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--disable-dev-shm-usage")
        chromeOptions.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path= os.environ.get("CHROMEDRIVER_PATH"),options=chromeOptions)
    sleep(3)

# Connect selenium to instagram   
def initBrowser():
    browser.get("https://www.instagram.com/?hl=fr")
    print("1 - Page Opened")
    sleep(10)
    browser.find_element_by_xpath("/html/body/div[4]/div/div/button[1]").click()
    sleep(2)
    print("2 - Cookies accepted")
    browser.find_element_by_name("username").send_keys(infos.user)
    browser.find_element_by_name("password").send_keys(infos.pwd)
    sleep(2)
    browser.execute_script('document.getElementsByTagName("button")[1].click()')
    sleep(10)
    browser.get("https://www.instagram.com/")
    print("3 - Connected")
    print(datetime.now())
    sleep(5)
    try:
        browser.execute_script('document.getElementsByTagName("button")[document.getElementsByTagName("button").length-1].click()')
    except:
        print("'plustard' notfound")



# Functions 

#Random sleep
def wait():
    sleep(random.randint(3,5))

# Function that fetch the oldest pending message from db

def fetchOldestPendingMessageFromDB():
    # Call API with params : status = 0, sort = ASC, limit = 1
    fetchedMessage = requests.get("https://la-boite-a-message.herokuapp.com/messages?_where[status]=0&_sort=created_at:ASC&_limit=1").json()
    # Check if fetchedMessage empty or not
    if fetchedMessage:
        # Return formated message with only usefull datas
        return [fetchedMessage[0]['id'],fetchedMessage[0]['target'],fetchedMessage[0]['message'],fetchedMessage[0]['socialnetwork']]
    else:
        return None

def change_status(id):
    # Change desired message status to '1' meaning sent
    requests.put(f"https://la-boite-a-message.herokuapp.com/messages{id}",
    data=json.dumps({
    'status': [1]
    }),
    headers={
    'Content-Type': 'application/json'
    })
    print('status_changed')

def change_status_error(id):
    # Change desired message status to '2' meaning error (emojis)
    requests.put(f"https://la-boite-a-message.herokuapp.com/messages{id}",
    data=json.dumps({
    'status': [2]
    }),
    headers={
    'Content-Type': 'application/json'
    })
    print('status_changed_err')

# Function that create the image for instagram post
def process_img(user):
    img = Image.open(f"{cwd}/data/image/letter.png")
    W = 1000
    if len(user)<=12:
        size = 100
    elif len(user)>12:
        size = int(100 - 3*(int(len(user)-12)))

    font = ImageFont.truetype(f"{cwd}/data/font/helvetica.ttf",size)
    process = ImageDraw.Draw(img)
    w, h = process.textsize(user,font=font)
    process.text(((W-w)/2,390),user,(120,120,120),font = font)
    process.text(((W-w)/2,385),user,(250,250,250),font = font)
    img.save(f"{cwd}/data/image/upload.png")

# Function that remove emojis
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

def post_message(id,user,msg):
    try:
        global browser
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
        browser.find_element_by_class_name("selected").send_keys(f"{cwd}/data/image/upload.png")
        print('- Image sent')
        wait()
        browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button').click()
        print('- Skip')
        wait()
        browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button').click()
        print('- Skip')
        wait()
        try:
            browser.find_element_by_xpath("/html/body/div[6]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/textarea").send_keys(f"@{user} : {msg}")
            print('- Text set')
        except Exception as e:
            print(f"[ERROR] {e}")
            change_status_error(id)
            return
        wait()
        browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/div/div/div[1]/div/div/div[2]/div/button').click()
        print('- Done')
        change_status(id)
    except Exception as e:
        print(f"[ERROR] {e}")

def time_sync():
    print("wait time sync with time")
    global browser

    while datetime.now().minute % 10 != 0:
         if datetime.now().minute == 45:
            print("Restart chrome instance")
            browser.quit()
            initSelenium()
            initBrowser()
            sleep(60)
    
    


initSelenium()
initBrowser()
while True:
    #time_sync()
    select_msg = fetchOldestPendingMessageFromDB()
    print(select_msg)
    # If 'select_msg' is empty then it return to while's starting
    if select_msg == None:
        print("continue")
        sleep(60)
        continue

    # If the message is for instagram then do :
    if select_msg[3] == 'instagram':
        # Process image
        process_img(select_msg[1])
        # Post      |    ID    |     |   TARGET  |    |  MESSAGE  |
        post_message(select_msg[0],select_msg[1],select_msg[2])
    
    if select_msg[3] == 'twitter':
        API.update_status(f"@{select_msg[1]} {select_msg[2]}")
        change_status(select_msg[0])
    sleep(60)
