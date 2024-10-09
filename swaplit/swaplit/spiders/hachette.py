import scrapy
import json
from ..items import EditorItem
from ..items import BookItem
from ..items import AuthorItem


class HachetteSpider(scrapy.Spider):
    name = "hachette"
    download_delay = 10
    allowed_domains = ["hachette.fr"]
    start_urls = ["https://www.hachette.fr/theme/beaux-livres", "https://www.hachette.fr/theme/histoire-de-lart-et-art-majeurs", "https://www.hachette.fr/theme/musique",
                  "https://www.hachette.fr/theme/bandes-dessinees", "https://www.hachette.fr/theme/mangas", "https://www.hachette.fr/theme/cuisine", "https://www.hachette.fr/theme/vins-et-spiritueux",
                  "https://www.hachette.fr/theme/fantastique", "https://www.hachette.fr/theme/fantasy", "https://www.hachette.fr/theme/science-fiction", "https://www.hachette.fr/theme/actualites",
                  "https://www.hachette.fr/theme/histoire", "https://www.hachette.fr/theme/ados", "https://www.hachette.fr/theme/albums-et-illustres", "https://www.hachette.fr/theme/eveil",
                  "https://www.hachette.fr/theme/premieres-encyclopedies", "https://www.hachette.fr/theme/premieres-lectures", "https://www.hachette.fr/theme/theatre-et-poesie", "https://www.hachette.fr/theme/biographies-memoires",
                  "https://www.hachette.fr/theme/essais", "https://www.hachette.fr/theme/humour", "https://www.hachette.fr/theme/oeuvres-classiques", "https://www.hachette.fr/theme/romans-et-nouvelles-de-genre",
                  "https://www.hachette.fr/theme/romans-etrangers", "https://www.hachette.fr/theme/romans-francophones", "https://www.hachette.fr/theme/romans-erotiques", "https://www.hachette.fr/theme/polar",
                  "https://www.hachette.fr/theme/thriller", "https://www.hachette.fr/theme/famille", "https://www.hachette.fr/theme/sante-bien-etre", "https://www.hachette.fr/theme/sports", "https://www.hachette.fr/theme/sciences",
                  "https://www.hachette.fr/theme/dictionnaires-et-encyclopedies", "https://www.hachette.fr/theme/droit-et-sciences-humaines", "https://www.hachette.fr/theme/geographie", "https://www.hachette.fr/theme/informatique-et-management",
                  "https://www.hachette.fr/theme/medecine", "https://www.hachette.fr/theme/religion", "https://www.hachette.fr/theme/scolaire-et-parascolaire", "https://www.hachette.fr/theme/cartes-et-atlas",
                  "https://www.hachette.fr/theme/guides", "https://www.hachette.fr/theme/bricolage", "https://www.hachette.fr/theme/loisirs", "https://www.hachette.fr/theme/nature"]
    page_nb = 1

    def parse(self, response):
        book_links = response.css('div.field-name-hw-livre-couverture a::attr(href)').getall()[1:]

        for book in book_links:
            yield response.follow(book, callback=self.parse_book)

        next_page = response.css('ul.pagination li a::attr(href)').getall()[self.page_nb]
        if self.page_nb == 1:
            self.page_nb += 3
        else:
            self.page_nb += 1

        yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        item = BookItem()

        item["title"] = response.css('div.field-name-hw-livre-titre-couv h1::text').get()
        item["author"] = response.css('div.group-info-livre div.field-name-hw-intervenants a::text').getall()
        item["summary"] = response.css('div.field-name-hw-presentation-editoriale div.field-item::text').get()
        item["EAN"] = response.css('div.field-name-hw-livre-ean div.field-item::text').get()
        # item["isbn"] = item['ean13'][0:3] + '-' + item['ean13'][3] + '-' + item['ean13'][4:6] + '-' + item['ean13'][6:12] + '-' + item['ean13'][12]
        item["editor"] = response.css('div.group-info-livre div.field-name-hw-editeurs a::text').get()
        item["publication_date"] = response.css('div.field-name-hw-livre-date-parution span.date-display-single::text').get()
        data_layer = response.css('script::text').re_first(r'dataLayer\s*=\s*(\[.*?\]);')
        try:
            data_layer_json = json.loads(data_layer)
            item["collection"] = data_layer_json[0].get("page_collections")[0]
        except:
            item['collection'] = []

        item["number_of_pages"] = response.css('div.field-name-hw-livre-nb-pages div.field-item::text').get()
        item["dimensions"] = response.css('div.field-name-hw-livre-format div.field-item::text').get()
        # item["poids"] = response.css('div.tab-content dd[itemtype="http://schema.org/Weight"]::text').get()
        item["language"] = "français"

        item['image_urls'] = [response.css(f'img[title="{item["title"]}"]::attr(src)').get()]

        yield item

        authors_url = response.css('div.group-info-livre div.field-name-hw-intervenants a::attr(href)').getall()
        editor_url = response.css('div.group-info-livre div.field-name-hw-editeurs a::attr(href)').get()

        for author in authors_url:
            yield response.follow(author, callback=self.parse_author)

        yield response.follow(editor_url, callback=self.parse_editor)

    def parse_author(self, response):
        item = AuthorItem()
        full_name = response.css('div.field-name-title-field h1::text').get().split(' ')
        # item['author_id'] = response.url.split('/')[-2]
        item['first_name'] = full_name[0]
        item['last_name'] = full_name[1]
        item['biography'] = response.css('div.field-name-hw-intervenant-biographie div.field-item::text').get()

        yield item

    def parse_editor(self, response):
        item = EditorItem()
        item['name'] = response.css('div.field-name-field-titre div.field-item::text').get()
        item['website_url'] = response.css('div.link-url a::attr(href)').get()
        item['image_urls'] = [response.css('div.field-name-hw-editeur-logo img[typeof="foaf:Image"]::attr(src)').get()]

        yield item
