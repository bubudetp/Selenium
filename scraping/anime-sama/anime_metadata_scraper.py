import sys
import os
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import random
import json
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import undetected_chromedriver as uc
from pprint import pprint
from utils.file_operation import write_to_file
from utils.string_operation import split_string_by_add, extract_number_from_anime_title
from utils.dict_operation import nautiljon_mapping, dict_map_field_names, genre_translation
from utils.constants import haikyuu
from colorama import Fore

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
nautiljon_base_url = "https://www.nautiljon.com/"

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

def process_anime_episodes(driver, url=None, anime_type="anime"):
    print(anime_type, "anime_type in episodes")

    if anime_type != "anime" and anime_type != "oav":
        return []
    
    if url:
        print(url, "printing the url")
        driver.get(url)
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='didomi-notice-agree-button']"))
        )
        accept_button.click()
        print("Clicked the consent button.")
    except Exception as e:
        print(f"Error clicking the consent button: {e}")
    
    try:
        
        episode_container_web_element = driver.find_element(By.ID, "episodes")
        metadata_episodes_container = episode_container_web_element.find_elements(By.TAG_NAME, "tr")
                
        episodes = []
        for episode_container in metadata_episodes_container:
            metadata_episode = {"episode_number": "", "fr_title": "", "eng_title": "", "pub_date": ""}
            
            td_elements = episode_container.find_elements(By.TAG_NAME, "td")
            
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
                    date_element = td_elements[-1]
                    if any(char.isdigit() for char in date_element.text):
                        metadata_episode["pub_date"] = date_element.text.strip()
                except Exception as e:
                    print(f"Error retrieving publication date: {e}")
            
            if any(value != "N/A" for value in metadata_episode.values()):
                episodes.append(metadata_episode)
            else:
                print(f"Skipping empty episode :{metadata_episode}")

            print("-" * 50)
    except Exception as e:
        print(f"Anime is an oav an only has one episode: ", e)
        return []

    return episodes

def process_seasons(anime, existing_titles=None):
    if existing_titles is None:
        existing_titles = set()
    else:
        existing_titles = set(existing_titles)
    print(existing_titles, "existing_titles")
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='didomi-notice-agree-button']"))
        )
        accept_button.click()
        print("Clicked the consent button.")
    except Exception as e:
        print(f"Error clicking the consent button: {e}")
        traceback.print_exc()
        
    anime_type_sequel = re.compile(r"(Série)")
    movie_type_sequel = re.compile(r"(Film)")

    anime_name = anime.get("name", "")
    liaisons_container = driver.find_element(By.ID, "liaisons")
    liaison_elements_web_containers = liaisons_container.find_elements(By.CLASS_NAME, "imagesBorder")
    anime_liaisons = {}
    expected_keyword = "animes"
    nb_of_season = anime.get("nb_of_season", 1)
    count = 1

    for liaisons in liaison_elements_web_containers:
        a = {"sequel_title": "", "sequel_type": "", "sequel_number": "", "sequel_img_url": "", "sequel_url": ""}

        try:
            anime_link = liaisons.find_element(By.TAG_NAME, "a")
            nautiljon_anime_url = anime_link.get_attribute("href")
            anime_title = anime_link.get_attribute("title")
            anime_img_url = liaisons.find_element(By.TAG_NAME, "img").get_attribute("src")
            type_text = liaisons.find_element(By.CSS_SELECTOR, "div.infos_small").text
            
            # Check for duplicates
            normalized_title = anime_title.lower().strip()
            if normalized_title in existing_titles:
                print(f"Duplicate sequel found: {anime_title}, skipping...")
                continue

            existing_titles.add(normalized_title)

            # Extract season or movie number
            sequel_number = extract_number_from_anime_title(anime_title, anime_name)

            # Verify URL structure
            print("checking for the sequel")
            base_url = "https://www.nautiljon.com/"
            if base_url in nautiljon_anime_url:
                remainder = nautiljon_anime_url.replace(base_url, "", 1)
            else:
                raise Exception(f"Base URL '{base_url}' not found in the given URL.")

            split_remainder = remainder.split('/')

            if split_remainder[0] == expected_keyword:
                print("The URL structure is as expected.")
            else:
                raise Exception(f"Sequel {split_remainder[1]} is not an Anime or a Manga")

            # Determine sequel type

            if anime_type_sequel.search(type_text):
                a["sequel_type"] = "anime"
                a["sequel_number"] = sequel_number
                nb_of_season += 1
            elif movie_type_sequel.search(type_text):
                a["sequel_type"] = "movie"
                a["sequel_number"] = sequel_number
            else:
                a["sequel_type"] = "oav"
                a["sequel_number"] = sequel_number

            print(anime_title, "anime_title")
            print(a["sequel_type"], "anime_type")
            
            a["sequel_title"] = anime_title
            a["sequel_img_url"] = anime_img_url
            a["sequel_url"] = nautiljon_anime_url
            anime["nautiljon_data"]["nb_of_season"] = nb_of_season

            anime_liaisons[count] = a
            count += 1
        except Exception as e:
            print(f"Error extracting anime details: {e}")
            traceback.print_exc()
            
            continue
    return anime_liaisons

def search_anime_name(anime_name):
    formatted_anime_name = split_string_by_add(anime_name)
    driver.get("https://www.nautiljon.com/animes/" + formatted_anime_name + ".html")

def scrape_anime_data(anime_name, anime_url=None):
    try:
        if anime_url is None:
            search_anime_name(anime_name)
        else:
            driver.get(anime_url)

        # Initialize the data structure
        anime_data = {
            "name": anime_name,
            "nautiljon_data": {
                "nb_of_season": 1,
                "sequels": {
                    "sequel_list": set()
                },
                "synopsis": [],
                "metadata": {},
                "average_rating": "No rating available",
                "member_count": "No member count available",
                "statistics": {},
                "img_url": "",
                "episodes": []
            }
        }

        synopsis = driver.find_element(By.CLASS_NAME, "description")
        anime_data["nautiljon_data"]["synopsis"] = [synopsis.text]

        metadata_lists_container = driver.find_element(By.CSS_SELECTOR, "ul.mb10")
        metadata_lists = metadata_lists_container.find_elements(By.TAG_NAME, "li")

        process_genres_and_themes(anime_data, metadata_lists)

        for list_item in metadata_lists:
            span_elements = list_item.find_elements(By.TAG_NAME, "span")
            if len(span_elements) >= 2:
                field_name = span_elements[0].text.rstrip(":").strip()
                value_text = [span.text for span in span_elements[1:]]
                anime_data["nautiljon_data"]["metadata"][field_name] = value_text
            elif len(span_elements) == 1:
                field_name = span_elements[0].text.rstrip(':').strip()
                if field_name not in ["Genres", "Thèmes"]:
                    full_text = list_item.text
                    following_text = full_text.replace(span_elements[0].text, '').strip()
                    anime_data["nautiljon_data"]["metadata"][field_name] = [following_text]
            else:
                try:
                    field_name = list_item.find_element(By.CSS_SELECTOR, 'span.bold').text.rstrip(':').strip()
                except:
                    field_name = list_item.text.split(':')[0].strip()

                if list_item.find_elements(By.TAG_NAME, 'a'):
                    links = list_item.find_elements(By.TAG_NAME, 'a')
                    link_texts = [link.text for link in links if link.text]
                    value_text = link_texts
                    anime_data["nautiljon_data"]["metadata"][field_name] = value_text
                else:
                    value_text = list_item.text.replace(field_name, '').strip()
                    anime_data["nautiljon_data"]["metadata"][field_name] = [value_text]

        try:
            rating_value = driver.find_element(By.CSS_SELECTOR, '[itemprop="ratingValue"]').text
            anime_data["nautiljon_data"]["average_rating"] = rating_value
        except:
            pass
        try:
            rating_count = driver.find_element(By.CSS_SELECTOR, '[itemprop="ratingCount"]').text
            anime_data["nautiljon_data"]["member_count"] = rating_count
        except:
            pass

        # Extract statistics
        statistics_star_web_element = driver.find_element(By.CSS_SELECTOR, "div.moyNote")
        statistics_rating_web_element = statistics_star_web_element.find_element(By.CSS_SELECTOR,"[itemprop='ratingValue']")

        statistics_ranks_web_element_container = driver.find_element(By.CSS_SELECTOR, "div.topsAll")
        statistics_rank_web_elements = statistics_ranks_web_element_container.find_elements(By.CSS_SELECTOR, "span.number")
        statistics_rank_names_web_elements = statistics_ranks_web_element_container.find_elements(By.CSS_SELECTOR, "a.tooltip")

        for i in range(len(statistics_rank_web_elements) - 1):
            anime_data["nautiljon_data"]["statistics"][statistics_rank_names_web_elements[i].text] = statistics_rank_web_elements[i].text
        anime_data["nautiljon_data"]["statistics"]["statistics_rating"] = statistics_rating_web_element.text

        # Extract image URL
        img_url_web_element = driver.find_element(By.CSS_SELECTOR, "a.cboxImage")
        anime_data["nautiljon_data"]["img_url"] = img_url_web_element.get_attribute("href")

        # Process episodes
        episodes = process_anime_episodes(driver)
        anime_data["nautiljon_data"]["episodes"] = episodes

        # Process sequels if applicable    
        anime_data["nautiljon_data"]["sequels"]["sequel_list"].add(anime_name)
        sequels = process_seasons(anime_data)
        for key, sequel in sequels.items():
            print("Processing sequel:", key)
            sequel_title_name = ""
            for k, value in sequel.items():
                if k == "sequel_title" and value:
                    sequel_title_name = value
                    anime_data["nautiljon_data"]["sequels"]["sequel_list"].add((value, True))
                    anime_data["nautiljon_data"]["sequels"].setdefault(sequel_title_name, {"episodes": []})
                
                if k == "sequel_type" and sequel_title_name:
                    try:
                        print(f"Fetching episodes for sequel: {sequel_title_name}")
                        processed_anime_name = nautiljon_base_url + "animes/" + split_string_by_add(sequel_title_name) + ".html"
                        episodes = process_anime_episodes(driver, processed_anime_name, value)
                        print(f"Episodes fetched: {episodes}")

                        anime_data["nautiljon_data"]["sequels"][sequel_title_name]["episodes"] = episodes
                        
                        sql_list = anime_data["nautiljon_data"]["sequels"]["sequel_list"]
                        
                        sql_index = sql_list.index(sequel_title_name)
                        sql_list.insert(sql_index, (sequel_title_name, False))
                        anime_data["nautiljon_data"]["sequels"]["sequel_list"] = sql_list
                        
                        
                        anime_data["nautiljon_data"]["sequels"][sequel_title_name]["nautiljon_data"] = scrape_anime_data(sequel_title_name, processed_anime_name)
                    except Exception as e:
                        print(f"Error processing sequel {sequel_title_name}: {e}")
                        traceback.print_exc()
                        continue
        print("returning anime data")
        return anime_data

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

        return None

def process_sequel_metadata(anime):
    if not anime:
        return
    
    anime_to_exclude = set(anime["nautiljon_data"]["sequels"]["sequel_list"])
    anime_name = anime.get("name")
    if anime_name and anime_name not in anime_to_exclude:
        anime_to_exclude.add(anime_name)
 
    sequels = anime.get("nautiljon_data", {}).get("sequels", {}).get("sequels_list", [])
    anime_sequels_url = []

    for seq in sequels:
        seq_title = seq.get("sequel_title")
        print(seq_title, "printing the sequel title")
        if seq_title not in anime_to_exclude:
            seq_type = seq.get("sequel_type")
            seq_url = seq.get("sequel_url")
            seq_number = seq.get("sequel_number")
            if seq_type == "anime" and seq_url:
                anime_sequels_url.append((seq_number, seq_title, seq_url))
    
    all_sequels_metadata = []

    for anime_sequel in anime_sequels_url:
        order, anime_title, anime_url = anime_sequel

        # Check if already processed
        if anime_title in anime_to_exclude:
            print(f"Already processed or excluded: {anime_title}, skipping...")
            continue

        anime_to_exclude.add(anime_title)
        anime_metadata = scrape_anime_data(anime_title, anime_url, True)
        if anime_metadata:
            anime["nautiljon_data"]["sequels"][f"{anime_title}"] = anime_metadata
            print(f"got metadata for {anime_title}")
        else:
            print(f"didnt get metadata for {anime_title}")

try:
    anime = scrape_anime_data("haikyu !!")
    write_to_file("x.json", anime)
    
    # process_sequel_metadata(anime)
    # write_to_file("anime_metadatass.json", anime)
    # process related animes
    driver.quit()

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
    
    driver.quit()

# season catcher, current system works
    
    # for these cases
        # 0. Initial = scrape all sequels + metadata of anime  
    #   : 1. loop = scrape metadata for sequal got in the initial scraping
    #     2. in the loop, scrape the sequels of the sequel got at each scraping and checks if the sequel has already been scraped or not
