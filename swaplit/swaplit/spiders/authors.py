import scrapy
from ..items import AuthorItem

class AuthorsSpyder(scrapy.Spider):
    name = "authors"

    start_urls = []
    authors_id = [
                    2021211,
                    2330766,
                    1113420,
                    997391,
                    1569712,
                    820295,
                    61093,
                    2029440,
                    2192971,
                    1950011,
                    1871152,
                    1850556,
                    556828,
                    1871118,
                    2094656,
                    145588,
                    971025,
                    769839,
                    1488584,
                    2377216,
                    1972169,
                    245919,
                    2386575,
                    2381712,
                    795153,
                    225616,
                    2367200,
                    2376703,
                    1915280,
                    1868242,
                    717064,
                    1714498,
                    1828544,
                    1194087,
                    1060502,
                    665368,
                    209446,
                    887186,
                    1600230,
                    1961275,
                    1807710,
                    2381040,
                    341651,
                    1345309,
                    1566040,
                    139514,
                    1678146,
                    1077869,
                    1842729,
                    2381749,
                    909314,
                    ]

    for author_id in authors_id:
        start_urls.append(f'https://www.leslibraires.fr/personne/{author_id}')

    def parse(self, response):
        item = AuthorItem()
        full_name = response.css('h1[itemprop="name"]::text').get().split(' ')
        item['author_id'] = response.url.split('/')[-2]
        item['first_name'] = full_name[0]
        item['last_name'] = full_name[1]
        item['biography'] = response.css('div[itemprop="description"] p::text').get()

        yield item
