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
# chrome_options.page_load_strategy = 'eager'

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



def get_url(td_elements):

    video_urls = {}
    pattern = re.compile(r'Saison (\d+) Episode (\d+)')

    for td in td_elements:
        link = td.find_element(By.CSS_SELECTOR, 'a')
        href = link.get_attribute('href')
        text = link.text
        desc = text.split('\n')

        match = pattern.search(desc[0])
        if match:
            episode_number = int(match.group(2))
            saison_number = int(match.group(1))
            if saison_number not in video_urls:
                video_urls[saison_number] = {}
            video_urls[saison_number][episode_number] = {
                "episode_number": episode_number,
                "link": href
            }
        else:
            print("not matched")

    sorted_video_urls = {season: {ep: video_urls[season][ep] for ep in sorted(video_urls[season])}
                         for season in sorted(video_urls)}
    

    print('sorted', sorted_video_urls)
    
    return sorted_video_urls


def get_videos(anime_name, td_elements):
    dic = {}
    dic = get_url(td_elements)

    video_urls = {anime_name: {}}
    for season, episodes in dic.items():
        video_urls[anime_name][season] = {}  # Initialize the season dictionary if not already present
        for episode, episode_data in episodes.items():
            print(f"Season: {season} Episode: {episode} Link: {episode_data['link']}")
            video_url = get_video_url(driver, episode_data['link'])
            video_urls[anime_name][season][episode] = video_url  # Assign the URL to the specific episode
    
    return video_urls

def get_video_url(driver, url):
    driver.get(url)
    html_link = driver.find_element(By.CSS_SELECTOR, '.code_for_insert A')
    html_link.click()
    print('Clicked on the link')    
    time.sleep(0.2)
    link = driver.find_element(By.CSS_SELECTOR, 'textarea')
    print(link.get_attribute("value"))

    return link.get_attribute("value")

def save_data_to_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)



def get_anime(anime_name, driver, actions):

    search_query = f'{anime_name} episode 1 vostfr'
    for letter in search_query:
        actions.send_keys(letter)
        human_like_delay(short=True)

    actions.perform()
    token = generateresponse(anchor_url, reload_url, payload)

    params = {
        'token': token 
    }
    response = requests.get(anchor_url, params=params)

    if response.status_code == 200:
        print("Success")
    
    human_like_delay()
    actions.send_keys(Keys.ENTER).perform()
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
                return True

            except TimeoutException:
                print("Bot challenge did not resolve in time. Retrying or handling differently.")
                break 
            except Exception as e:
                print(f"Unexpected error interacting with bot challenge: {e}")
                break 

    except TimeoutException:
        print("No bot challenge detected, proceeding.")
        return True
    
try:
    driver.get(url)
    start = time.time()
    print('Program Started')
    width = random.randint(1024, 1920)
    height = random.randint(768, 1080)
    driver.set_window_size(width, height)
    time.sleep(2) 

    actions = ActionChains(driver)

    for _ in range(random.randint(3, 7)):
        actions.move_by_offset(random.randint(0, 50), random.randint(0, 50))
        if random.choice([True, False]):
            actions.click()
        actions.perform()
        human_like_delay(short=True)

    human_like_delay()
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "top_search_main_input"))
    )
    
    actions.move_to_element(search_box).click().perform()
    human_like_delay(short=True)

    anime_name = 'One Piece'

    if get_anime(anime_name, driver, actions):
        td_elements = driver.find_elements(By.CSS_SELECTOR, 'td.text')
        video_urls = get_videos(anime_name, td_elements)

        save_data_to_json('data.json', video_urls)
        end = time.time()
        elapsed = (end - start) / 60
        print('(time taken)', elapsed)

finally:
    driver.quit()






