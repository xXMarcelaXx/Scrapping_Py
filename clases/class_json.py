import json

class JsonConfigReader:
    @staticmethod
    def read_config(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
