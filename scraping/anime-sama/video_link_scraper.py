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

base_url = "https://anime-sama.fr/catalogue/"

def scroll_to_bottom():
    """Scroll to the bottom of the page to ensure all content is loaded."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for content to load


def translate_genres_or_themes(text_list):
    return [genre_translation.get(text, text) for text in text_list]

def process_genres_and_themes(anime, metadata_lists):
    for list_item in metadata_lists:
        span_elements = list_item.find_elements(By.TAG_NAME, "span")
        if span_elements:
            field_name = span_elements[0].text.rstrip(':').strip()
            if field_name in ["Genres", "Thèmes"]:
                if list_item.find_elements(By.TAG_NAME, 'a'):
                    links = list_item.find_elements(By.TAG_NAME, 'a')
                    link_texts = [link.text for link in links if link.text]
                    translated_texts = translate_genres_or_themes(link_texts)
                    anime["nautiljon_data"][field_name] = translated_texts

def get_description(anime, driver):
    text = driver.find_element(By.CSS_SELECTOR, "div.description")
    anime["nautiljon_data"]["synopsis"] = [text.text]
    print(text.text, "odpoifdopfk[paosfkp[oasedk[p]]]")

def scrape_anime_names(anime_name):
    try:
        formatted_anime_name = split_string_by_add(anime_name)
        driver.get("https://www.nautiljon.com/animes/" + formatted_anime_name + ".html")
        anime = {"name": anime_name, "nautiljon_data": {}}
        
        time.sleep(2)
        
        metadata_lists_container = driver.find_element(By.CSS_SELECTOR, "ul.mb10")
        metadata_lists = metadata_lists_container.find_elements(By.TAG_NAME, "li")
        synopsis = driver.find_element(By.CSS_SELECTOR, "div.description")
        anime["nautiljon_data"]["synopsis"] = [synopsis.text]

        process_genres_and_themes(anime, metadata_lists)

        for list_item in metadata_lists:
            span_elements = list_item.find_elements(By.TAG_NAME, "span")
            if len(span_elements) >= 2:
                field_name = span_elements[0].text.rstrip(":").strip()
                value_text = [span.text for span in span_elements[1:]]
                anime["nautiljon_data"][field_name] = value_text
            elif len(span_elements) == 1:
                field_name = span_elements[0].text.rstrip(':').strip()
                if field_name not in ["Genres", "Thèmes"]:  # Exclude already processed fields
                    full_text = list_item.text
                    following_text = full_text.replace(span_elements[0].text, '').strip()
                    anime["nautiljon_data"][field_name] = [following_text]
            else:
                try:
                    field_name = list_item.find_element(By.CSS_SELECTOR, 'span.bold').text.rstrip(':').strip()
                except:
                    # In case there is no span.bold, we use a different approach
                    field_name = list_item.text.split(':')[0].strip()

                # Handling links with nested spans for other fields
                if list_item.find_elements(By.TAG_NAME, 'a'):
                    links = list_item.find_elements(By.TAG_NAME, 'a')
                    link_texts = [link.text for link in links if link.text]
                    value_text = link_texts
                    anime["nautiljon_data"][field_name] = value_text
                else:
                    value_text = list_item.text.replace(field_name, '').strip()
                    anime["nautiljon_data"][field_name] = [value_text]

        try:
            rating_value = driver.find_element(By.CSS_SELECTOR, '[itemprop="ratingValue"]').text
            anime["nautiljon_data"]["average_rating"] = [rating_value]
        except:
            anime["nautiljon_data"]["average_rating"] = ["No rating available"]

        try:
            rating_count = driver.find_element(By.CSS_SELECTOR, '[itemprop="ratingCount"]').text
            anime["nautiljon_data"]["member_count"] = [rating_count]
        except:
            anime["nautiljon_data"]["member_count"] = ["No member count available"]

        # Extract the synopsis if it exists on the page
        
        statistics_star_web_element = driver.find_element(By.CSS_SELECTOR, "div.moyNote")
        statistics_rating_web_element = statistics_star_web_element.find_element(By.CSS_SELECTOR,"[itemprop='ratingValue']")
        
        statistics_ranks_web_element_container = driver.find_element(By.CSS_SELECTOR, "div.topsAll")
        statistics_rank_web_elements = statistics_ranks_web_element_container.find_elements(By.CSS_SELECTOR, "span.number")
        statistics_rank_names_web_elements = statistics_ranks_web_element_container.find_elements(By.CSS_SELECTOR, "a.tooltip")

        statistics = {}
        for i in range(len(statistics_rank_web_elements) - 1):
            statistics[statistics_rank_names_web_elements[i].text] = statistics_rank_web_elements[i].text
        statistics["statistics_rating"] = statistics_rating_web_element.text

        img_url_web_element = driver.find_element(By.CSS_SELECTOR, "a.cboxImage")
        anime["nautiljon_data"]["statistics"] = statistics
        anime["nautiljon_data"]["img_url"] = [img_url_web_element.get_attribute("href")]
        
        pprint(anime)

        anime["nautiljon_data"] = dict_map_field_names(anime["nautiljon_data"], nautiljon_mapping)
    except Exception as e:
        print(f"An error occurred: {e}")

try:
    scrape_anime_names("bleach")

except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()
