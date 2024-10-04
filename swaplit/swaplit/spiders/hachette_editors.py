import scrapy
from ..items import EditorItem

class HachetteEditorsSpider(scrapy.Spider):
    name = "hachette_editors"
    download_delay = 10
    allowed_domains = ["hachette.fr"]
    start_urls = ["https://www.hachette.fr/editeurs"]

    def parse(self, response):
        editor_links = response.css('div.field-name-hw-editeur-logo a::attr(href)').getall()

        for editor in editor_links:
            yield response.follow(editor, callback=self.parse_editor)


    def parse_editor(self, response):
        item = EditorItem()
        item['name'] = response.css('div.field-name-field-titre div.field-item::text').get()
        item['website_url'] = response.css('div.link-url a::attr(href)').get()
        item['image_urls'] = [response.css('div.field-name-hw-editeur-logo img[typeof="foaf:Image"]::attr(src)').get()]

        yield item
