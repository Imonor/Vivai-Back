"""File containing services for Supported Plants"""

from multiprocessing import Process, Manager

from botocore.exceptions import ClientError


import common.utilities as utilities
import common.plant_services as plant_services
import common.db_dealer as db_dealer

from scrapy import signals
from plant_info.plant_info.spiders.plant_info_spider import PlantInfoSpider


import scrapy.crawler as crawler
from twisted.internet import reactor

from scrapy.signalmanager import dispatcher

PARAM_SPECIES = "species"

def get_plant_infos(species):
    """Checks if species parameter has completed infos in Plant table.
    If not it completes the plant infos by web-scrapping method and returns the plant ID.
    Else it returns the plant ID without web-scrapping"""

    try:
        item = db_dealer.get_attributes(db_dealer.PLANT_TABLE, ["id", "picUrl"], "species", "=", species)

        # Espèce de plante non renseignée dans la table informative
        if not item:
                       
            returned_url = db_dealer.get_item(db_dealer.SUPPORTED_PLANT_TABLE, species, "","", ["websiteUrl"])["websiteUrl"]["S"]
            
            def f(return_list):
                def collect_items(signal, sender, item, response, spider):
                    return_list.append(item)
                dispatcher.connect(collect_items, signal=signals.item_passed)
                runner = crawler.CrawlerRunner()
                deferred = runner.crawl(PlantInfoSpider, url=returned_url)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()

            manager = Manager()
            return_list = manager.list()
            p = Process(target=f, args=(return_list,))
            p.start()
            p.join()

            items = return_list[0]
            picUrl = items.get('picUrl')
            # Ajout de la plante dans la table informative et retour de son ID.

            try:
                plant_id = plant_services.add_plant(items)
                return plant_id, picUrl

            except ClientError as error:
                raise error

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
