# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SwaplitItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    book_title = scrapy.Field()
    author = scrapy.Field()
    author_id = scrapy.Field()
    informations = scrapy.Field()
    ean13 = scrapy.Field()
    isbn = scrapy.Field()
    editeur = scrapy.Field()
    publication_date = scrapy.Field()
    collection = scrapy.Field()
    page_number = scrapy.Field()
    dimensions = scrapy.Field()
    poids = scrapy.Field()
    language = scrapy.Field()
