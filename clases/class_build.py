import pandas as pd
import os
import logging

class BuildData():
    def __init__(self, data_dict={}, file_path='./', file_name='pags'):
        self.file_path = file_path
        self.file_name = file_name
        self.df = pd.DataFrame(data_dict)
        logging.basicConfig(level=logging.INFO)



    def export_to_excel(self, file_name=None):
        print(self.df)
        if not isinstance(self.df, pd.DataFrame):
            logging.error("self.df is not a pandas DataFrame.")
            return
        directory = self.file_path
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, file_name or self.file_name + '.xlsx')
        try:
            self.df.to_excel(file_path, index=False)
            logging.info(f"Datos exportados a Excel en: {file_path}")
        except Exception as e:
            logging.error(f"Error guardando a Excel: {e}")

    def data (self):
        return self.df
    


