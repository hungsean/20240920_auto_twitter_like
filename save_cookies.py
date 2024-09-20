import os
import pickle
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logs_dir = os.getenv('LOGS_DIR', 'logs')
os.makedirs(logs_dir, exist_ok=True)
log_filename = os.path.join(logs_dir, 'save_cookies.log')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_filename),
                        logging.StreamHandler()
                    ])

def save_cookies():
    chromedriver_path = os.getenv('CHROMEDRIVER_PATH', 'chromedriver.exe')
    target_url = os.getenv('TARGET_URL', 'https://x.com/home')
    cookies_file = os.getenv('COOKIES_FILE', 'cookies.pkl')

    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service)

    try:
        logging.info(f"Opening target website: {target_url}")
        driver.get(target_url)

        input("Once manual actions are completed, press Enter to save Cookies...")

        cookies = driver.get_cookies()
        with open(cookies_file, 'wb') as file:
            pickle.dump(cookies, file)

        logging.info(f"Cookies successfully saved to {cookies_file}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        driver.quit()
        logging.info("Browser session ended")

if __name__ == "__main__":
    save_cookies()