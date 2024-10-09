import yaml

class CategoryHelper:
    def __init__(self, spider_name):
        self.__categories_file = '../categories/' + spider_name + '-categories.yaml'

        with open(self.__categories_file, 'r') as file:
            self.__category_service = yaml.safe_load(file)

    def map_scraped_category(self, scraped_category):
        return self.__category_service['categories'].get(scraped_category)
