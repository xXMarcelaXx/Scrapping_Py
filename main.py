from clases.class_actions import WebScrapping
from clases.class_build import BuildData
from clases.class_json import JsonConfigReader

def main(config):
    web_scrapper = WebScrapping()
    web_scrapper.init(config)
    web_scrapper.perform_actions()
    web_scrapper.close_driver()
    data = web_scrapper.all_data
    if data:
        print(config['name'])
        data_builder = BuildData(data, file_path='excel')
        data_builder.export_to_excel(config['name_excel'])


if __name__ == '__main__':
    config_files = ['json/configEbay.json', 'json/configTiobe.json', 'json/configCNN.json']
    for config_file in config_files:
        config = JsonConfigReader.read_config(config_file)
        main(config)
