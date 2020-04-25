"""File containing services for Supported Plants"""

from botocore.exceptions import ClientError
import common.db_dealer as db_dealer
import common.utilities as utilities
import common.plant_services as plant_services

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
        if (len(response["records"]) == 0):
            # Code pour le web-scrapping
            
            # Ajout de la plante dans la table informative et retour de son ID.
            # res_add = plant_services.add_plant(attributes)
            # return utilities.generate_http_response(res_add["generatedFields"][0]["longValue"])
            
            # Pour l'instant, web-scrapping non implémenté.
            return {"Message" : "Web-scrapping nécéssaire"}

        # Espèce déjà renseignée dans la table informative
        else:
            return {"plantId": response["records"][0][0]["longValue"]}
        
    except ClientError as error:
        return utilities.handle_error(error)

def get_supported_plants(event, context):
    """Returns the list of the supported plants"""
    try:
        parameters = utilities.get_parameters(event, [], [PARAM_SEARCH])
        search = parameters[PARAM_SEARCH]

    except utilities.MissingParameterException:
        search = ""

    try:
        sql_statement = f'SELECT species, websiteUrl FROM {db_dealer.DATABASE}.{db_dealer.SUPPORTED_PLANT_TABLE}'
        if search:
            sql_statement += f' WHERE species LIKE "%{search}%"'
        sql_statement += f' ORDER BY species;'
        response = db_dealer.execute_statement(sql_statement)

        supported_plants = []
        for record in response['records']:
            plant = {
                "species": record[0]['stringValue'],
                "websiteUrl": record[1]['stringValue']
            }
            supported_plants.append(plant)

        return utilities.generate_http_response(supported_plants)

    except ClientError as error:
        return utilities.handle_error(error)
