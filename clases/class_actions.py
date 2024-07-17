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


class WebScrapping:
    def init(self, config):
        logging.basicConfig(level=logging.INFO)
        self.config = config
        self.options = Options()
        self.options.headless = True
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-extensions')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)

    def get_data(self):
        try:
            self.driver.get(self.config['url'])
            if 'actions' in self.config:
                self.actions()
            return self.extract_data()
        except Exception as e:
            logging.error(f"Error loading page: {e}")
            return None
        
    def extract_data(self, table_data = None):
        if table_data is None:
            table_data = [] 
        try:
            table = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.config['main_element'])))
            if 'header_selector' in self.config:
                headers = [header.text for header in table.find_elements(By.CSS_SELECTOR, self.config['header_selector'])]
                table_data.insert(0, headers)
            rows = table.find_elements(By.CSS_SELECTOR, self.config['row'])
            
            for i in range(min(self.config.get('num_items', len(rows)), len(rows))):
                row = rows[i]
                if 'cell_selector' in self.config:
                    cells = row.find_elements(By.CSS_SELECTOR, self.config['cell_selector'])
                    row_data = [cell.text for cell in cells]
                    table_data.append(row_data)
                  
                elif 'fields' in self.config:
                    row_data = {}
                    for field, selector in self.config['fields'].items():
                        elements = row.find_elements(By.CSS_SELECTOR, selector)
                        row_data[field] = elements[0].text.strip() if elements else None
                    table_data.append(row_data)
            return self.convert_to_dict(table_data)
        except Exception as e:
            logging.error(f"Error extracting data: {e}")
        
    def actions(self):
        try:
            for accion in self.config.get('actions', []):
                wait_time = accion.get('wait', 20)
                elements = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, accion['selector'])))
            if accion['type'] == 'input':
                elements.send_keys(accion['value'])
                elements.send_keys(Keys.RETURN)
            elif accion['type'] == 'click':
                elements.click()
            elif accion['type'] == 'submit':
                elements.send_keys(Keys.RETURN)
        except TimeoutException as e:
            logging.error(f"Timeout esperando elemento: {accion['selector']} - {e}")
        except NoSuchElementException as e:
            logging.error(f"Elemento no encontrado: {accion['selector']} - {e}")
        except Exception as e:
            logging.error(f"Error en las acciones: {e} - Acción: {accion}")

    def convert_to_dict(self, data):
        try:
            if not isinstance(data[0], dict):
                return [{data[0][i]: data[j][i] for i in range(len(data[0])) if data[j][i] != ''} for j in range(1, len(data))]
            return data
        except Exception as e:
            logging.error(f"Error converting data to dict: {e}")
            return None
        
    
    def close_driver(self):
        self.driver.quit()