import yaml
import os

class CategoryHelper:
    def __init__(self, spider_name):
        self.__categories_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'categories', spider_name + '-categories.yaml')

        with open(self.__categories_file, 'r') as file:
            self.__category_service = yaml.safe_load(file)

    def map_scraped_category(self, scraped_category):
        return self.__category_service['categories'].get(scraped_category)
