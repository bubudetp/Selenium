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

try:
    urls = [
        "https://video.sibnet.ru/alb669286-Tokyo_Revengers/",
        "https://video.sibnet.ru/alb686008-Otonari_no_Tenshi_sama_ni_Itsunomanika_Dame_Ningen_ni_Sareteita_Ken/",
        "https://video.sibnet.ru/alb683686-Blue_Lock/",
        "https://video.sibnet.ru/alb684459-Chainsaw_Man_VF/",
        "https://video.sibnet.ru/alb683828-Chainsaw_Man/",
        "https://video.sibnet.ru/alb683744-Fuufu_Ijou__Koibito_Miman/",
        "https://video.sibnet.ru/alb678208-SPY_x_FAMILY/",
        "https://video.sibnet.ru/alb678209-Ao_Ashi/",
        "https://video.sibnet.ru/alb677941-Tomodachi_Game/",
        "https://video.sibnet.ru/alb666921-Mushoku_Tensei/",
        "https://video.sibnet.ru/alb673337-Kimetsu_no_Yaiba_S2/",
        "https://video.sibnet.ru/alb673306-Blue_Period/",
        "https://video.sibnet.ru/alb648222-Vinland_Saga/",
        "https://video.sibnet.ru/alb668322-Kimetsu_no_Yaiba_vf/",
        "https://video.sibnet.ru/alb667066-Dr_Stone_2/"
    ]

    anime_series = {}

    for anime_url in urls:
        driver.get(anime_url)
        
        width = random.randint(1024, 1920)
        height = random.randint(768, 1080)
        driver.set_window_size(width, height)
        
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, 'h1')
            title = title_element.text
        except Exception as e:
            print(f"Could not find title for URL {anime_url}: {e}")
            continue  

        anime_series[title] = []
        video_links = driver.find_elements(By.CSS_SELECTOR, 'div.name a')
        for link_element in video_links:
            link = link_element.get_attribute('href')
            anime_series[title].append(link)


    with open('anime_series.json', 'a') as file:  # Use 'a' to append or 'w' to overwrite
        json.dump(anime_series, file, ensure_ascii=False, indent=4)

except Exception as e:
    print(f"Error: {e}")


    