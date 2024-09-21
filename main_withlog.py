import os
import pickle
import time
import sqlite3
import requests
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logs_dir = os.getenv('LOGS_DIR', 'logs')
os.makedirs(logs_dir, exist_ok=True)
log_filename = os.path.join(logs_dir, datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.log')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_filename),
                        logging.StreamHandler()
                    ])

# Environment Variables
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH', 'chromedriver.exe')
TARGET_URL = os.getenv('TARGET_URL', 'https://x.com/home')
COOKIES_FILE = os.getenv('COOKIES_FILE', 'cookies.pkl')
MEDIA_DB_PATH = os.getenv('MEDIA_DB_PATH', 'databases/media_data.db')
IMAGES_DIR = os.getenv('IMAGES_DIR', 'images_png')
LIKES_URL = os.getenv('LIKES_URL', 'https://x.com/senen_3454/likes')

# Initialize the database
def init_db(db_path):
    logging.info(f"Initializing database at {db_path}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            post_id TEXT NOT NULL,
            photo_index TEXT NOT NULL,
            media_id TEXT NOT NULL UNIQUE,
            download_time DATETIME
        )
    ''')
    conn.commit()
    logging.info("Database initialized successfully")
    return conn, cursor

# Insert data into the database
def insert_media_data(cursor, data):
    try:
        cursor.execute('''
            INSERT INTO media (user_name, post_id, photo_index, media_id, download_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['user_name'], data['post_id'], data['photo_index'], data['media_id'], data.get('download_time')))
        logging.info(f"Inserted media_id {data['media_id']} into the database")
    except sqlite3.IntegrityError:
        logging.info(f"media_id {data['media_id']} already exists. Skipping insert.")

# Save and close the database
def save_and_close_db(conn):
    conn.commit()
    conn.close()
    logging.info("Database connection closed")

# Process an <a> tag to extract information
def process_a_tag(a_tag):
    result = {}
    logging.info("Processing <a> tag")

    try:
        href = a_tag.get_attribute('href')
        if href:
            href_path = href.split('?')[0].split('#')[0].split('/')
            if len(href_path) >= 8:
                result['user_name'] = href_path[3] if len(href_path) > 3 else None
                result['post_id'] = href_path[5] if len(href_path) > 5 else None
                result['photo_index'] = href_path[7] if len(href_path) > 7 else None

        try:
            # Explicit wait for <img> tag to load
            img_tag = WebDriverWait(a_tag, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'img'))
            )
            if img_tag:
                src = img_tag.get_attribute('src')
                if src:
                    src_path = src.split('?')[0].split('#')[0].split('/')
                    if len(src_path) > 4:
                        result['media_id'] = src_path[4] if len(src_path) > 4 else None
        except TimeoutException:
            logging.warning("Timeout waiting for <img> tag in <a> tag")

    except Exception as e:
        logging.error(f"Error processing <a> tag: {e}")

    result['download_time'] = datetime.now()
    logging.info(f"Processed <a> tag: {result}")
    return result

# Filter <a> tags to find media links
def filter_a_tags(links):
    logging.info("Filtering <a> tags")
    result_links = []
    for link in links:
        href = link.get_attribute('href')
        if href:
            href_parts = href.split('/')
            if len(href_parts) > 7 and href_parts[4] == 'status' and href_parts[6] == 'photo':
                result_links.append(link)
    logging.info(f"Filtered {len(result_links)} <a> tags")
    return result_links

# Download image by media ID
def download_image(image_id):
    logging.info(f"Downloading image {image_id}")
    url = f'https://pbs.twimg.com/media/{image_id}?format=png&name=4096x4096'

    os.makedirs(IMAGES_DIR, exist_ok=True)
    image_path = os.path.join(IMAGES_DIR, f'{image_id}.png')

    if os.path.exists(image_path):
        logging.info(f"Image {image_id} already exists at {image_path}. Skipping download.")
        return

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        logging.info(f"Image {image_id} downloaded successfully to {image_path}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download image {image_id}: {e}")

# Save the filtered data and download images
def save_data(a_tags):
    logging.info("Saving data")
    filtered_a_tags = filter_a_tags(a_tags)

    if filtered_a_tags:
        conn, cursor = init_db(MEDIA_DB_PATH)
        for a_tag in filtered_a_tags:
            try:
                result = process_a_tag(a_tag)
                logging.info(f"Result from processing: {result}")

                if result.get('media_id'):
                    insert_media_data(cursor, result)
                    download_image(result['media_id'])
            except Exception as e:
                logging.error(f"Error processing link: {e}")
        save_and_close_db(conn)
    else:
        logging.info("No <a> tags found matching criteria")

# Set up the Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Enable headless mode
    chrome_options.add_argument('--no-sandbox')  # Avoid sandbox issues
    chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid filesystem issues

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Main function to control the process
def main():
    logging.info("Starting the web scraping process")
    driver = setup_driver()

    try:
        driver.get(TARGET_URL)
        logging.info(f"Opened the home page: {TARGET_URL}")

        with open(COOKIES_FILE, 'rb') as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        logging.info("Cookies loaded and applied")

        driver.get(LIKES_URL)
        logging.info(f"Navigated to the target page: {LIKES_URL}")

        while True:

            # Logging the current page URL
            current_url = driver.current_url
            logging.info(f"Current page URL: {current_url}")

            time.sleep(5)
            all_a_tags = driver.find_elements(By.TAG_NAME, 'a')
            save_data(all_a_tags)

            for _ in range(3):
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
            logging.info("Scrolled down the page")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        driver.quit()
        logging.info("Web scraping process completed")

if __name__ == "__main__":
    main()
