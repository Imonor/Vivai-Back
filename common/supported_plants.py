"""File containing services for Supported Plants"""

from botocore.exceptions import ClientError


import common.utilities as utilities
import common.plant_services as plant_services
import common.db_dealer as db_dealer

from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess
from plant_info.plant_info.spiders.plant_info_spider import PlantInfoSpider

PARAM_SPECIES = "species"

def get_plant_infos(species):
    """Checks if species parameter has completed infos in Plant table.
    If not it completes the plant infos by web-scrapping method and returns the plant ID.
    Else it returns the plant ID without web-scrapping"""

    try:
        item = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["id", "picUrl"], "species", "=", species)

        # Espèce de plante non renseignée dans la table informative
        if not item:
            # Code pour le web-scrapping : 
            returned_url = db_dealer.get_item(db_dealer.SUPPORTED_PLANT_TABLE, species, "","", ["websiteUrl"])["websiteUrl"]["S"]

            items = []
            def collect_items(item, response, spider):
                items.append(item)

            crawler = Crawler(PlantInfoSpider)
            crawler.signals.connect(collect_items, signals.item_scraped)
            process = CrawlerProcess()
            process.crawl(crawler, url= returned_url)  
            process.start()
            items = items[0]
            picUrl = items.get('picUrl')
            # Ajout de la plante dans la table informative et retour de son ID.

            plant_id = plant_services.add_plant(items)

            return plant_id, picUrl

        # Espèce déjà renseignée dans la table informative

        return item["id"]["S"], item["picUrl"]["S"]

    except ClientError as error:
        raise error

def get_supported_plants(event, context):
    """Returns the list of the supported plants"""
    try:
        supported_plants = db_dealer.get_all_items(db_dealer.SUPPORTED_PLANT_TABLE)
        for plant in supported_plants:
            plant["species"] = plant["species"]["S"]
            plant.pop("websiteUrl")

        return utilities.generate_http_response(supported_plants), 200

    except ClientError as error:
        return utilities.handle_error(error)
