"""File containing services for Supported Plants"""

from botocore.exceptions import ClientError

import common.utilities as utilities
import common.db_dealer as db_dealer
from plant_info.plant_info.spiders.plant_info_spider import PlantInfoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

PARAM_SEARCH = "search"
PARAM_SPECIES = "species"

def get_plant_infos(species):
    """Checks if species parameter has completed infos in Plant table.
    If not it completes the plant infos by web-scrapping method and returns the plant ID.
    Else it returns the plant ID without web-scrapping"""
    
    try:
        item = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["id", "picUrl"], "species", "=", species)

        # Espèce de plante non renseignée dans la table informative
        if not item:
            # Code pour le web-scrapping
            process = CrawlerProcess(get_project_settings())
            process.crawl('plantInfo', url='https://jardinage.ooreka.fr/plante/voir/16/basilic')
            process.start() # the script will block here until the crawling is finished

            # Ajout de la plante dans la table informative et retour de son ID.
            
            # res_add = plant_services.add_plant(attributes)
            # return utilities.generate_http_response(res_add["generatedFields"][0]["longValue"])
            
            return item

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
            plant["websiteUrl"] = plant["websiteUrl"]["S"]

        return utilities.generate_http_response(supported_plants), 200

    except ClientError as error:
        return utilities.handle_error(error)
