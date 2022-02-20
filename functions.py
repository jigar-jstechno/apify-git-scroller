# from msilib.schema import Directory
from email.policy import default
from itertools import count
import os
from time import sleep
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
from apify_client import ApifyClient
import sys
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import asyncio
import subprocess
import test
# import chromeweb as ch

# ch.WebDriver()
client = ApifyClient(os.environ['APIFY_TOKEN'], api_url=os.environ['APIFY_API_BASE_URL'])

# Get the resource subclient for working with the default key-value store of the actor
default_kv_store_client = client.key_value_store(os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID'])

# Get the value of the actor input and print it
actor_input = default_kv_store_client.get_record(os.environ['APIFY_INPUT_KEY'])['value']
print('Actor input:')
print(json.dumps(actor_input, indent=2))

default_kv_store_client.set_record('OUTPUT', actor_input)

# Get the resource subclient for working with the default dataset of the actor
default_dataset_client = client.dataset(os.environ['APIFY_DEFAULT_DATASET_ID'])

print(os.environ['APIFY_API_BASE_URL'],'api_url')
# print(default_kv_store_client,'kv')
# print(default_kv_store_client.id,'kvid')
# Push some dummy items to the default dataset





# with WebDriver() as driver:
#     driver.login()



# _GIF_NAME = actor_input._GIF_NAME
# _URL = actor_input._URL
# _WINDOW_W = actor_input._WINDOW_W
# _WINDOW_H = actor_input._WINDOW_H
# _START_Y = actor_input._START_Y
# _STOP_Y = actor_input._STOP_Y
# _FINAL_W = actor_input._FINAL_w
# _FINAL_H = actor_input._FINAL_H
# _SCROLL_STEP = actor_input._SCROLL_STEP
# _TIME_PER_FRAME = actor_input._TIME_PER_FRAME
_GIF_NAME = ("site1.gif")
_URL = "http://hando-pre-demo-template-pitchlane.webflow.io/?record-id=recTn4em3bKYgW6m7"
_WINDOW_W = ("1920")
_WINDOW_H = ("1080")
_START_Y = ('0')
_STOP_Y = 0
_FINAL_W = ("640")
_FINAL_H = ("360")
_SCROLL_STEP = ("25")
_TIME_PER_FRAME = ("100")
temp=0
_DRIVER = test.d

try:
    path = os.path.join(os.getcwd(), 'images')
    os.mkdir(path)
except:
    pass


# def start_driver():
#     """Start Selenium driver."""
#     global _URL

    # options = webdriver.ChromeOptions()
    # options = Options()
    # # options.use_chromium = True

    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("start-maximized")
    # options.add_argument("disable-infobars")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-gpu")
    
    # options.add_argument(f"--width={_WINDOW_W}")
    # options.add_argument(f"--height={_WINDOW_H}")
print(os.getcwd())
# chrome_driver_binary = "/usr/src/app/chromedriver"
#options.binary_location=chrome_driver_binary

# ls_output=subprocess.Popen([chrome_driver_binary])
path='ls'
# path1='cd /usr/bin/'
# path2='cd ..'
# os.system(path1)
os.system(path)
# os.system(path2)
# os.system(path2)
# s=os.system(chrome_driver_binary)
# cap = DesiredCapabilities().CHROME.copy() 
# cap["marionette"] = False
# cap['acceptInsecureCerts'] = True
# _DRIVER = webdriver.Firefox(
#     capabilities=cap,
#     executable_path=r""+os.getcwd()+"/geckodriver",
#     options=options,
#     service_log_path="geckodriver.log",
# ) 

# /usr/src/app/geckodriver
# _DRIVER = webdriver.Chrome(options=Options, executable_path = chromedriver_autoinstaller.install(cwd=True))
# _DRIVER = ChromeDriverManager(executable_path = s)
#executable_path=chrome_driver_binary,
# _DRIVER = webdriver.Chrome('chromedriver')
# CHROMEDRIVER = '/chromedriver'
# options = Options()
# options.add_argument("--headless")

# _DRIVER = webdriver.Chrome(CHROMEDRIVER, options=Options)
# _DRIVER.implicitly_wait(10)
print(_URL)
_DRIVER.get("https://google.com")
sleep(5)


def close_driver():
    global _DRIVER
    """Stop Selenium driver."""
    _DRIVER.close()
    _DRIVER.quit()


def take_screenshot(num: int):
    global _DRIVER
    # import random
    # value = random.random(1, 100)
    """Save current page display as a .png
    Args:
        num (int): Screenshot number.
    Returns:
        str: Screenshot save path.
    """
    path = "images/screenshots{}.png".format(str(num))
    _DRIVER.save_screenshot(path)

    return path


def validate_stop_y():
    _STOP_Y = temp

    page_height = _DRIVER.execute_script(
        "return document.body.parentNode.scrollHeight")

    if _STOP_Y == 0:
        _STOP_Y = int(page_height)
        print(f" - STOP Y not defined, _STOP_Y set to {_STOP_Y}")
    elif _STOP_Y > int(page_height):
        _STOP_Y = page_height
        print(f" - STOP Y greater than page height, _STOP_Y set to {_STOP_Y}")


def scroll_page():
    global _DRIVER

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
    # print(screenshot_list)

    print(f" - {str(len(screenshot_list))} screenshots taken")

    return screenshot_list


def process_frame(file: str):
    global _DRIVER
    """Open screenshot file as a Pillow Image object and resize it.
    Args:
        file (str): Local screenshot path.
    Returns:
        Image: Pillow Image object.
    """
    image = Image.open(file)
    image = image.resize(
        size=(int(_FINAL_W), int(_FINAL_H)),
        resample=Image.LANCZOS,
        reducing_gap=3,
    )

    return image


def create_gif(screenshots: list):
    global _DRIVER
    """Use Pillow to create GIF.
    Args:
        screenshots (list): List of taken screenshots local files.
    """
    fp_out = "site1.gif"
    img, *imgs = map(process_frame, screenshots)
    img.save(
        fp=fp_out,
        format="GIF",
        append_images=imgs,
        save_all=True,
        duration=int(_TIME_PER_FRAME),
        loop=0,
        optimize=False,
    )
#start_driver()
screenshots = scroll_page()
l = len(screenshots)
l = l/2
l = int(l)
s = screenshots[0]
k = screenshots[l]
for i in range(10):
    screenshots.insert(l, k)
for i in range(10):
    screenshots.insert(2, s)
close_driver()
create_gif(screenshots=screenshots)
os.system(path)
# Set the 'OUTPUT' key-value store record to the same value as the input

filename="site1.gif"

file1 = open(filename,"r+") 
  
# print("Output of Read function is ")
# print(file1.read())
default_kv_store_client.set_record('gif', file1.read())

# Get the resource subclient for working with the default dataset of the actor
default_dataset_client = client.dataset(os.environ['APIFY_DEFAULT_DATASET_ID'])

# print(os.environ['APIFY_API_BASE_URL'],'api_url')
# print(default_kv_store_client,'kv')
# print(default_kv_store_client.id,'kvid')
# Push some dummy items to the default dataset
objc=[
    {'site_gif': 'https://api.apify.com/v2/key-value-stores/'+os.environ['APIFY_DEFAULT_KEY_VALUE_STORE_ID']+'/records/gif'},
    {'column1': 'dummy1b', 'column2': 'dummy2b'},
]
print(objc)
default_dataset_client.push_items(objc)