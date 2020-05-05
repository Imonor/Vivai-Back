#type in 2:Python:
#PS C:\PLD SMART\Vivai-Back\hello\plantDemo\plantDemo\spiders> scrapy crawl plants

import scrapy

class PlantListSpider(scrapy.Spider):
    name = 'plantDB'

    start_urls = [
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/a',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/b',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/c',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/d',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/e',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/f',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/g',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/h',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/i',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/j',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/k',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/l',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/m',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/n',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/o',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/p',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/q',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/r',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/s',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/t',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/u',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/v',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/w',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/x',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/y',
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/z',
    ]

    def parse(self, response):
        
        for plant in response.css('div.info_plante'):
            url = plant.css('a.titre_liste_plante::attr(href)').get()
            species = plant.css('a.titre_liste_plante::text').get()
            yield { "species": {"S":  species}, "websiteUrl": {"S": "https://jardinage.ooreka.fr"+ url}}
                # next_page = /page-{}/ where {} number of page.
        next_page_short = response.xpath('//*[@id="plant-search-result"]/div[21]/div[3]/a/@href').extract_first()

        # If next_page have value
        if next_page_short is not None:
            next_page =  "https://jardinage.ooreka.fr" + next_page_short
            # Recall parse with url https://sanet.st/page-{}/ where {} number of page.
            yield scrapy.Request(url=next_page, callback=self.parse)
