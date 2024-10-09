import json
from pathlib import Path
from urllib import request
import scrapy
from ..items import BookItem

class BookSpider(scrapy.Spider):
    name = "book"
    allowed_domains = ["leslibraires.fr", "images-na.ssl-images-amazon.com"]
    start_urls = ["https://www.leslibraires.fr/livre/23662610-frapper-l-epopee-alice-zeniter-flammarion"]

    def parse(self, response):
        item = BookItem()

        item["title"] = response.css('h1 span[itemprop="name"]::text').get()
        item["author"] = response.css('h2 a[itemprop="author"]::text').get()
        # item["author_id"] = response.css('h2 a[itemprop="author"]::attr(href)').get().split('/')[3]
        item["summary"] = response.css('[id="infos-description"]::text').get()
        item["EAN"] = response.css('div.tab-content dd::text')[1].get()
        item["isbn"] = response.css('div.tab-content dd[itemprop="isbn"]::text').get()
        item["editor"] = response.css('div.tab-content dd[itemprop="publisher"] a::text').get()
        item["publication_date"] = response.css('div.tab-content dd[itemprop="datePublished"]::text').get()
        item["collection"] = response.css('div.tab-content dd a::text')[2].get()
        item["number_of_pages"] = response.css('div.tab-content dd[itemprop="numberOfPages"]::text').get()
        item["dimensions"] = response.css('div.tab-content dd::text')[9].get()
        item["weight"] = response.css('div.tab-content dd[itemtype="http://schema.org/Weight"]::text').get()
        item["language"] = response.css('div.tab-content dd[itemprop="inLanguage"]::text').get()

        image_urls_response = request.urlopen(f'https://bookcover.longitood.com/bookcover/{response.css('div.tab-content dd::text')[1].get()}')
        image_urls = json.loads(image_urls_response.read().decode('utf-8'))
        if image_urls['url'] == 'https://images-na.ssl-images-amazon.com/images/S/compressed.photo.goodreads.com/books/1708576099i/208998628.jpg':
            image_urls['url'] = ''



        item['image_urls'] = [image_urls['url']]

        yield item

        # Call the endpoint to get the recommendations HTML
        recommendations_url = "https://www.leslibraires.fr/recommendations/?ean13="+response.css('div.tab-content dd::text')[1].get()
        recommendations_response = request.urlopen(recommendations_url)
        recommendations_data = json.loads(recommendations_response.read().decode('utf-8'))

        # Parse the HTML to extract URLs
        recommendations_html = recommendations_data["html"]
        recommendations_response = scrapy.http.HtmlResponse(url="dummy", body=recommendations_html, encoding='utf-8')
        url_list = recommendations_response.css('li a::attr(href)').getall()[1:]

        for url in url_list:
            yield response.follow(url, callback=self.parse)
