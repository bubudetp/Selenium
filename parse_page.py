from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc
import time
import config
import re
import time
import random
import requests
import json 

def rand_proxy():
    proxy_details = random.choice(config.ips)
    return {
        'http': f'http://{proxy_details}',
        'https': f'https://{proxy_details}',
        'no_proxy': 'localhost,127.0.0.1'
    }

url = "https://video.sibnet.ru/"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

user_agent = random.choice(USER_AGENTS)
chrome_options = uc.ChromeOptions()
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.page_load_strategy = 'eager'

proxy = rand_proxy()

driver = uc.Chrome(options=chrome_options, seleniumwire_options={'proxy': proxy})

anchor_url = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcQNSYkAAAAAF1GWlXnMCZUbHx1DyMRwzrgM7kR&co=aHR0cHM6Ly92aWRlby5zaWJuZXQucnU6NDQz&hl=en&v=YurWEBlMIwR4EqFPncmQTkxQ&size=invisible&cb=3kwzvqnfehy0"

reload_url = "https://www.google.com/recaptcha/api2/reload?k=6LcQNSYkAAAAAF1GWlXnMCZUbHx1DyMRwzrgM7kR"

payload = "v=YurWEBlMIwR4EqFPncmQTkxQ&reason=q&c=<token>&k=6LcQNSYkAAAAAF1GWlXnMCZUbHx1DyMRwzrgM7kR&co=aHR0cHM6Ly92aWRlby5zaWJuZXQucnU6NDQz&hl=en&size=invisible&chr=&vh=&bg=" 

def generateresponse(anchorurl, reloadurl, payload):
    s = requests.Session()
    r1 = s.get(anchorurl).text
    token1 = r1.split('recaptcha-token" value="')[1].split('">')[0]
    payload = payload.replace("<token>", str(token1))
    r2 = s.post(reloadurl, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        token2 = str(r2.text.split('"rresp","')[1].split('"')[0])
        return token2
    except:
        return ""
    
def get_all_anime_data(json_file_path):
    with open(json_file_path, 'r') as file:
        anime_data = json.load(file)

    all_data = {}
    for title, links in anime_data.items():
        all_data[title] = links

    return all_data

def human_like_delay(short=False):
    if short:
        time.sleep(random.uniform(0.5, 1.5))
    else:
        time.sleep(random.uniform(1, 3))


def handle_bot(driver):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.robot')))
        print("Bot challenge detected.")
        while True:
            try:
                link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.robot a')))
                link.click()
                print("Clicked on the link")
                
                WebDriverWait(driver, 10).until_not(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.robot')))
                print("Bot challenge resolved or page updated.")
                break 

            except TimeoutException:
                print("Bot challenge did not resolve in time. Retrying or handling differently.")
                break 
            except Exception as e:
                print(f"Unexpected error interacting with bot challenge: {e}")
                break 
            print("Bot solved")

    except TimeoutException:
        print("No bot challenge detected, proceeding.")


def get_video_url(driver, url):
    driver.get(url)
    html_link = driver.find_element(By.CSS_SELECTOR, '.code_for_insert A')
    title = driver.find_element(By.CSS_SELECTOR, 'td.video_name a ').text
    print(title)
    html_link.click()
    print("Clicked on the link")
    link = driver.find_element(By.CSS_SELECTOR, 'textarea')
    return link.get_attribute('value')

# link, anime_name = get_video_url(driver, "https://video.sibnet.ru/video5196957-Vinland_Saga_S2_24_VOSTFR/")

def get_anime_name(driver, url):
    driver.get(url)
    anime_name = driver.find_element(By.CSS_SELECTOR, 'h1').text
    return anime_name

def save_data_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

anime_data = get_all_anime_data("anime_series.json")

video_urls= {}

for title, episodes in anime_data.items():
    if title not in video_urls:
        video_urls[title] = []

    for episode_url in episodes:
        video_url = get_video_url(driver, episode_url)
        video_urls[title].append(video_url)

save_data_to_json('Animes.json', video_urls)