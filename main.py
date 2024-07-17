from clases.class_actions import WebScrapping
from clases.class_build import BuildData

def main(config):
    web_scrapper = WebScrapping()
    web_scrapper.init(config)
    data = web_scrapper.get_data()
    web_scrapper.close_driver()
    
    if data:
        print(config['name'])
        data_builder = BuildData(data, file_path='excel',)
        data_builder.export_to_excel(config['name_excel'])


if __name__ == '__main__':
    configEbay = {
        'name': 'Ebay',
        'name_excel': 'Ebay.xlsx',
        'url': 'https://mx.ebay.com/',
        'actions': [
            {'selector': 'input.gh-tb.ui-autocomplete-input', 'type': 'input', 'value': 'star wars lego'},
        ],
        'main_element': 'ul.srp-results.srp-grid.clearfix',
        'row': 'li.s-item.s-item__pl-on-bottom',
        'fields': {
            'Nombre': 'span[role="heading"]',
            'Estado': 'span.SECONDARY_INFO',
            'Precio': 'span.s-item__price',
        },
        'num_items': 10,
    }
    configTiobe = {
        'name': 'Tiobe',
        'name_excel': 'Tiobe.xlsx',
        'url': 'https://www.tiobe.com/tiobe-index/',
        'main_element': 'table.table-striped.table-top20',
        'header_selector': 'thead tr th',
        "row": "tbody tr",
        "cell_selector": "td",
        "num_items": 10     
    }
    configCNN = {
        'name': 'CNN',
        'name_excel': 'CNN.xlsx',
        'url': 'https://cnnespanol.cnn.com  ',
        'main_element': 'div.row.dp_zn0',
        'row': 'article.news.news--box.news--box-style-two.news--summary.news--summary-destacado.news--105x60.news--with-border-bottom.post-type--post',
        'fields': {
            'Titulo': 'span.news__label',
            'Descripcion': 'h2.news__title',
        },
        'num_items': 4,
    }
    main(configEbay)
    main(configTiobe)
    main(configCNN)
