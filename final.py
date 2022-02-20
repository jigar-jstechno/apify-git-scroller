from email.policy import default
from itertools import count
import os
from time import sleep
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import asyncio
import subprocess
import test 
from apify_client import ApifyClient
import pandas as pd
import base64
import requests
from pygifsicle import optimize
import shutil

# import cookies


client = ApifyClient(os.environ['APIFY_TOKEN'], api_url=os.environ['APIFY_API_BASE_URL'])
default_kv_store_client = client.key_value_store(os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID'])
actor_input = default_kv_store_client.get_record(os.environ['APIFY_INPUT_KEY'])['value']
# print('Actor input:')
# print(json.dumps(actor_input, indent=2))
default_kv_store_client.set_record('OUTPUT', actor_input)
default_dataset_client = client.dataset(os.environ['APIFY_DEFAULT_DATASET_ID'])



lossy_out = "final_image_lossy.gif"
losless_out='final_image_losless.gif'
_URL = actor_input["url"]
# print(_URL)
_WINDOW_W = actor_input["viewportWidth"]
_WINDOW_H = actor_input["viewportHeight"]
_START_Y = ("0")
_STOP_Y = ("0")
_FINAL_W = "640"
_FINAL_H = "360"
if _WINDOW_W:
    _FINAL_W = _WINDOW_W
if _WINDOW_H:
    _FINAL_H = _WINDOW_H
    
if actor_input["scrollDown"]==False:
    _FINAL_H="1000000"

_FINAL_W = "640"
_FINAL_H = "360"

_SCROLL_STEP = actor_input["scrollPercentage"]
_TIME_PER_FRAME = actor_input["frameRate"]
waitToLoad=actor_input["waitToLoadPage"]
cook=""
if "cookieWindowSelector" in actor_input:
    cook=actor_input["cookieWindowSelector"]
_DRIVER = test.d
lossy=actor_input["loslessCompression"]
losless=actor_input["loslessCompression"]
if lossy==False and losless==False:
    losless=True

try:
    path = os.path.join(os.getcwd(), 'images')
    os.mkdir(path)
except:
    pass

def start_driver():
    try:
        _DRIVER.get(_URL)
    except:
        _DRIVER.add_cookie(cook)
    sleep(waitToLoad)
    
   
def close_driver():
    _DRIVER.close()
    _DRIVER.quit()

def take_screenshot(num: int):
    print("Taking Screenshot")
    path = "images/screenshots{}.png".format(str(num))
    _DRIVER.save_screenshot(path)
    return path


def validate_stop_y():
    global _STOP_Y
    _STOP_Y=int(_STOP_Y)
    page_height = _DRIVER.execute_script(
        "return document.body.parentNode.scrollHeight")
    if _STOP_Y == 0:
        _STOP_Y = int(page_height)
        print(f" - STOP Y not defined, _STOP_Y set to {_STOP_Y}")
    elif _STOP_Y > int(page_height):
        _STOP_Y = page_height
        print(f" - STOP Y greater than page height, _STOP_Y set to {_STOP_Y}")

def scroll_page():
    SCROLL_PAUSE_TIME = 20
    validate_stop_y()
    _DRIVER.execute_script(f"window.scrollTo(0, {_START_Y})")
    _DRIVER.implicitly_wait(2)
    screenshot_list = [take_screenshot(num=0)]
    current_y = int(_START_Y)

    while current_y < _STOP_Y:
        current_y += int(_SCROLL_STEP)
        _DRIVER.execute_script(f"window.scrollTo(0, {str(current_y)})")
        screenshot = take_screenshot(num=len(screenshot_list))
        screenshot_list.append(screenshot)
    print(f" - {str(len(screenshot_list))} screenshots taken")
    return screenshot_list


def process_frame(file: str):
    image = Image.open(file)
    image = image.resize(
        size=(int(_FINAL_W), int(_FINAL_H)),
        resample=Image.LANCZOS,
        reducing_gap=3,
    )
    return image


def create_gif(screenshots: list):
    lossy_out = "final_image_lossy.gif"
    losless_out = "final_image_losless.gif"
    img, *imgs = map(process_frame, screenshots)
    img.save(
        fp=losless_out,
        format="GIF",
        append_images=imgs,
        save_all=True,
        duration=int(_TIME_PER_FRAME),
        loop=0,
        optimize=False,
    )
    if lossy==True:
        img.save(
            fp=lossy_out,
            format="GIF",
            append_images=imgs,
            save_all=True,
            duration=int(_TIME_PER_FRAME),
            loop=0,
            optimize=True,
        )

    

start_driver()
screenshots = scroll_page()
l = len(screenshots)
l = l/2
sc= int(l/10)
l = int(l)
s = screenshots[1]
k = screenshots[l]
for i in range(sc):
    screenshots.insert(l, k)
for i in range(sc):
    screenshots.insert(2, s)
close_driver()
create_gif(screenshots=screenshots)

#shutil.copyfile(lossy_out, losless_out)
# if str(lossy)==True:



if lossy==True:
    optimize(lossy_out)
    with open(lossy_out, "rb") as f:
        im_bytes = f.read()        
    im_b64 = base64.b64encode(im_bytes).decode("utf8")

    default_kv_store_client.set_record(lossy_out,im_bytes)#file1.read()


if losless==True:
    with open(losless_out, "rb") as f:
        im_bytes1 = f.read()        
    im_b641 = base64.b64encode(im_bytes1).decode("utf8")
    # default_kv_store_client.set_record('gif',"data:image/gif;base64,"+ im_b64)#file1.read()
    default_kv_store_client.set_record(losless_out,im_bytes1)#file1.read()

onjc=[]

if losless==True and lossy==True:
    objc=[
        {'lossy': 'https://api.apify.com/v2/key-value-stores/'+os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID']+'/records/'+lossy_out,'losless': 'https://api.apify.com/v2/key-value-stores/'+os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID']+'/records/'+losless_out},
    ]
   

elif losless==True:
    objc=[
        {'losy': 'https://api.apify.com/v2/key-value-stores/'+os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID']+'/records/'+lossy_out}
    ]
      
elif lossy==True:
    objc=[
        {'losless': 'https://api.apify.com/v2/key-value-stores/'+os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID']+'/records/'+losless_out}
    ]

default_dataset_client.push_items(objc)
#print(objc)
print("Finished")


# objc=[
#     {'site_gif': 'https://api.apify.com/v2/key-value-stores/'+os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID']+'/records/final_image.gif','column2': 'dummy2a'},
#     {'column1': 'dummy1b', 'column2': 'dummy2b'},
# ]
# print(objc)
# default_dataset_client.push_items(objc)