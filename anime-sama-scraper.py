from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException
import undetected_chromedriver as uc
from utils.file_operation import write_to_file
import random
import json

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

def get_page_links():
    try:
        page_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.p-3"))
        )
        return [link.get_attribute('href') for link in page_links]
    except TimeoutException as te:
        print(f"Timeout while getting page links: {te}")
        return []

def scrape_anime_names(page_links):
    for link in page_links:
        try:
            driver.get(link)
            print(f"Navigating to: {link}")

            # Wait for the new page to load by checking for a known element on the new page
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.font-semibold"))
            )

            # Fetch elements from the new page
            title_elements = driver.find_elements(By.CSS_SELECTOR, "h1.font-semibold")
            print("Title elements found:", len(title_elements))
            
            for title in title_elements:
                anime_name = title.text
                print(anime_name)
                write_to_file("catalogue.json", {"url": link, "anime_name": anime_name})
            
            driver.back()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.p-3")))

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
    for page_number in range(1, 31):  # Adjust the range as needed
        driver.get(base_url + f"index.php?page={page_number}")
        print(f"Page {page_number} loaded successfully.")

        # Close any overlay if present
        close_overlay()

        # Get all links on the page
        page_links = get_page_links()
        print(f"Links found on page {page_number}: {len(page_links)}")

        # Process each link
        scrape_anime_names(page_links)
    
    driver.quit()
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()
