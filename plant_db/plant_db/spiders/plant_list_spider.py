#type in 2:Python:
#PS C:\PLD SMART\Vivai-Back\hello\plantDemo\plantDemo\spiders> scrapy crawl plants

import scrapy

class PlantListSpider(scrapy.Spider):
    name = 'plantDB'

    start_urls = [
        'https://jardinage.ooreka.fr/plante/rechercheAlpha/a',
    ]

    def parse(self, response):
        plantList = {}
        i = 0
        for plant in response.css('div.info_plante'):
            url = plant.css('a.titre_liste_plante::attr(href)').get()
            species = plant.css('a.titre_liste_plante::text').get()
            plantList[i] = "{ \"species\": {\"S\": " + species + "}, \"websiteUrl\": {\"S\": https://jardinage.ooreka.fr"+ url + "} }"
            i = i + 1
        
        return plantList