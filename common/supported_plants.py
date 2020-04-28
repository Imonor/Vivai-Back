"""File containing services for Supported Plants"""

from botocore.exceptions import ClientError
import common.db_dealer as db_dealer
import common.utilities as utilities

PARAM_SEARCH = "search"
PARAM_SPECIES = "species"

def get_plant_id(species):
    """Checks if species parameter has completed infos in Plant table.
    If not it completes the plant infos by web-scrapping method and returns the plant ID.
    Else it returns the plant ID without web-scrapping"""
    
    try:
        sql_statement = f'SELECT id FROM {db_dealer.DATABASE}.{db_dealer.PLANT_TABLE} \
            WHERE species = "{species}";'

        response = db_dealer.execute_statement(sql_statement)

        # Espèce de plante non renseignée dans la table informative
        if not response["records"]:
            # Code pour le web-scrapping
            
            # Ajout de la plante dans la table informative et retour de son ID.
            # res_add = plant_services.add_plant(attributes)
            # return utilities.generate_http_response(res_add["generatedFields"][0]["longValue"])
            
            # Pour l'instant, web-scrapping non implémenté.
            return {"Message" : "Web-scrapping nécéssaire"}

        # Espèce déjà renseignée dans la table informative
        
        return {"plantId": response["records"][0][0]["longValue"]}
        
    except ClientError as error:
        return utilities.handle_error(error)

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
