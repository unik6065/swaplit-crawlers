# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    EAN = scrapy.Field()
    title = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    author = scrapy.Field()
    editor = scrapy.Field()
    collection = scrapy.Field()
    # author_id = scrapy.Field()
    publication_date = scrapy.Field()
    summary = scrapy.Field()
    number_of_pages = scrapy.Field()
    dimensions = scrapy.Field()
    weight = scrapy.Field()
    language = scrapy.Field()


class AuthorItem(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    biography = scrapy.Field()

class EditorItem(scrapy.Item):
    name = scrapy.Field()
    website_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
