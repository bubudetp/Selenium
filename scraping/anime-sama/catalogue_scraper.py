from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import undetected_chromedriver as uc
from utils.file_operation import write_to_file
import random
import json
import time

def write_to_file(filename, data):
    try:
        with open(filename, 'a') as f:
            json.dump(data, f, indent=4)
            f.write('\n')
    except Exception as e:
        print(f"Failed to write to file: {e}")

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

def close_overlay():
    try:
        overlay = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "qc-cmp2-ui"))
        )
        close_button = overlay.find_element(By.CSS_SELECTOR, "button[mode='secondary']")
        close_button.click()
        WebDriverWait(driver, 10).until(EC.invisibility_of_element(overlay))
    except TimeoutException:
        print("No overlay present or could not find the close button.")
    except Exception as e:
        print(f"Error closing overlay: {e}")

def scroll_to_bottom():
    """Scroll to the bottom of the page to ensure all content is loaded."""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for content to load

def get_last_page_number():
    try:
        pagination_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.p-3"))
        )
        last_page_link = pagination_links[-1]
        last_page_number = int(last_page_link.text)
        return last_page_number
    except (TimeoutException, ValueError) as e:
        print(f"Error determining the last page number: {e}")
        return 1  # Default to 1 if unable to determine

def get_page_links():
    try:
        page_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.p-3"))
        )
        return [link.get_attribute('href') for link in page_links]
    except TimeoutException as te:
        print(f"Timeout while getting page links: {te}")
        return []

def scrape_anime_names(link):
    try:
        driver.get(link)
        print(f"Navigating to: {link}")

        scroll_to_bottom()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.font-semibold"))
        )

        title_elements = driver.find_elements(By.CSS_SELECTOR, "h1.font-semibold")
        print("Title elements found:", len(title_elements))
        
        for title in title_elements:
            anime_name = title.text
            print(anime_name)
            write_to_file("catalogue.json", {"url": link, "anime_name": anime_name})

    except StaleElementReferenceException:
        print(f"Stale element reference for link: {link}. No retry.")
    except ElementClickInterceptedException:
        print(f"Element click intercepted for link: {link}. Retrying after closing overlay.")
        close_overlay()
    except TimeoutException as te:
        print(f"Timeout while processing link: {link} - {te}")
    except Exception as e:
        print(f"An error occurred: {e}")

try:
    driver.get(base_url + "index.php?page=1")
    print("Main page loaded successfully.")

    # Close any overlay if present
    close_overlay()

    last_page_number = get_last_page_number()
    print(f"Last page number: {last_page_number}")

    for page_number in range(1, last_page_number + 1):
        page_link = base_url + f"index.php?page={page_number}"
        print(f"Page {page_number} loaded successfully.")

        close_overlay()

        # Process each link
        scrape_anime_names(page_link)
    
    driver.quit()
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()
