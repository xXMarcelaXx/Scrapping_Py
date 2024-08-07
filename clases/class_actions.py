from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

class WebScrapping:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.driver = None
        self.config = None
        self.all_data = []

    def init(self, config):
        self.config = config
        self.options = Options()
        self.options.headless = True
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-extensions')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)

    def perform_actions(self):
        try:
            for action in self.config['actions']:
                if action['action'] == 'get':
                    self.driver.get(action['url'])
                elif action['action'] == 'write':
                    self.write(action)
                elif action['action'] == 'click':
                    self.click(action)
                elif action['action'] == 'extract':
                    data = self.extract_data(action)
                    if data:
                        self.all_data.extend(data)
                time.sleep(action.get('wait', 1))  # Espera opcional entre acciones
        except Exception as e:
            logging.error(f"Error performing actions: {e}")

    def write(self, action):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((self.get_by(action['selector']['by']), action['selector']['value']))
            )
            element.send_keys(action['text'])
        except Exception as e:
            logging.error(f"Error writing text: {e}")

    def click(self, action):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((self.get_by(action['selector']['by']), action['selector']['value']))
            )
            element.click()
        except Exception as e:
            logging.error(f"Error clicking element: {e}")

    def extract_data(self, action):
        data = []
        try:
            table = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((self.get_by(action['table']['by']), action['table']['value']))
            )
            rows = table.find_elements(By.XPATH if action['row'].startswith('//') else By.CSS_SELECTOR, action['row'])
            for row in rows:
                row_data = {}
                for cell in action['cells']:
                    cell_element = row.find_element(By.XPATH if cell['selector'].startswith('//') else By.CSS_SELECTOR, cell['selector'])
                    row_data[cell['name']] = cell_element.text.strip() if cell_element else None
                data.append(row_data)
        except Exception as e:
            logging.error(f"Error extracting data: {e}")
        return data

    def get_by(self, by):
        return {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }[by]

    def close_driver(self):
        if self.driver:
            self.driver.quit()