from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
import logging
import pandas as pd
import os
from utils.json_handler import JSONHandler


# Configurar el driver de Chrome
options = Options()
options.headless = True
#Para que el navegador se abra en pantalla grande
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Configurar el logging
logging.basicConfig(level=logging.INFO)

# Definir la clase DataBuilder
class DataBuilder(JSONHandler):
    def __init__(self, data_dict={}, file_path='./', file_name='pags'):
        super().__init__(file_path, file_name)
        self.df = pd.DataFrame(data_dict)

    def export_to_excel(self, file_name=None):
        file_path = os.path.join(self.file_path, file_name or self.file_name + '.xlsx')
        try:
            self.df.to_excel(file_path, index=False)
            logging.info(f"Data saved to Excel at {file_path}")
        except Exception as e:
            logging.error(f"Error saving to Excel: {e}")

try:
    driver.get("https://mx.ebay.com/")

    # Esperar a que aparezca el input de búsqueda y enviar "star wars lego"
    input_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.gh-tb.ui-autocomplete-input"))
    )
    input_element.send_keys("star wars lego")

    # Enviar el formulario
    input_element.submit()

    # Esperar a que aparezcan los resultados principales
    main_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.srp-results.srp-grid.clearfix"))
    )

    # Encontrar los primeros 5 resultados
    items = main_element.find_elements(By.CSS_SELECTOR, "li.s-item.s-item__pl-on-bottom")[:5]
    data = []

    for item in items:
        # Extraer los campos especificados
        nombre = item.find_element(By.CSS_SELECTOR, "span[role='heading']").text
        estado = item.find_element(By.CSS_SELECTOR, "span.SECONDARY_INFO").text
        precio = item.find_element(By.CSS_SELECTOR, "span.s-item__price").text

        # Imprimir los resultados
        print(f"Nombre: {nombre}")
        print(f"Estado: {estado}")
        print(f"Precio: {precio}")
        print("-" * 40)
        data.append({"Nombre": nombre, "Estado": estado, "Precio": precio})

    # Crear una instancia de DataBuilder con los datos extraídos
    data_builder = DataBuilder(data)

    # Exportar los datos a un archivo Excel
    data_builder.export_to_excel("ebay_results.xlsx")

finally:
# Cerrar el navegador al finalizar
    print("Cerrando navegador...")