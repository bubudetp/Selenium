import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import undetected_chromedriver as uc
from pprint import pprint
from utils.file_operation import write_to_file
from utils.string_operation import split_string_by_add
from utils.dict_operation import nautiljon_mapping, dict_map_field_names, genre_translation

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

driver = uc.Chrome(options=chrome_options)

driver.get("https://www.nautiljon.com/animes/bleach.html")

# Wait for the button to be clickable and then click it
try:
    # Wait for the 'Accepter & Fermer' button to be clickable
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='didomi-notice-agree-button']"))
    )
    accept_button.click()
    print("Clicked the consent button.")
except Exception as e:
    print(f"Error clicking the consent button: {e}")

episode_container_web_element = driver.find_element(By.ID, "episodes")
metadata_episodes_container = episode_container_web_element.find_elements(By.TAG_NAME, "tr")
print(len(metadata_episodes_container), "len")
time.sleep(10)
        
episodes = []
for episode_container in metadata_episodes_container:
    metadata_episode = {"episode_number": "", "fr_title": "", "eng_title": "", "pub_date": ""}
    
    td_elements = episode_container.find_elements(By.TAG_NAME, "td")
    print(f"Number of td elements: {len(td_elements)}")
    
    if len(td_elements) > 1:
        metadata_episode["episode_number"] = td_elements[0].text.strip() if td_elements[0].text.strip() else "N/A"
        
        try:
            fr_title_element = td_elements[1].find_element(By.TAG_NAME, "p")
            metadata_episode["fr_title"] = fr_title_element.text.strip() if fr_title_element.text.strip() else "N/A"
        except Exception as e:
            print(f"Error retrieving French title: {e}")
        
        try:
            en_title_element = td_elements[1].find_element(By.TAG_NAME, "a")
            metadata_episode["eng_title"] = en_title_element.text.strip() if en_title_element.text.strip() else "N/A"
        except Exception as e:
            print(f"Error retrieving English title: {e}")
        
        try:
            # Assuming the last `td` contains the publication date
            date_element = td_elements[-1]
            if any(char.isdigit() for char in date_element.text):
                metadata_episode["pub_date"] = date_element.text.strip()
        except Exception as e:
            print(f"Error retrieving publication date: {e}")
    
    if any(value != "N/A" for value in metadata_episode.values()):
        episodes.append(metadata_episode)
    else:
        print(f"Skipping empty episode: {metadata_episode}")

    print("-" * 50)

write_to_file("episodes.json", episodes)