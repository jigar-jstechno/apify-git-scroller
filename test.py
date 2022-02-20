from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from apify_client import ApifyClient


#print("start")
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
d = webdriver.Chrome('/opt/chromedriver',options=chrome_options)
#d.get('https://www.google.com/')
#print("end")