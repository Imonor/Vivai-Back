"""File containing services for Supported Plants"""

from botocore.exceptions import ClientError
import common.db_dealer as db_dealer
import common.utilities as utilities
import common.plant_services as plant_services

PARAM_SEARCH = "search"
PARAM_SPECIES = "species"

def get_plant_id(event, context):
    """Checks if supported species as completed infos :
        if not : complete the plant infos by web scrapping method and returns the plant id
        else : returns the plant id"""
    try:
        parameters = utilities.get_parameters(event, [PARAM_SPECIES], [])
        species = parameters[PARAM_SPECIES]

        sql_statement = f'SELECT id FROM {db_dealer.DATABASE}.{db_dealer.PLANT_TABLE} \
            WHERE species = "{species}";'

        response = db_dealer.execute_statement(sql_statement)

        # Espèce de plante non renseignée dans la table informative
        if (len(response["records"]) == 0):
            # Code pour le web-scrapping

            # Attributs retournés par défaut pour l'instant
            attributes = {
                "species": "WebScrapper",
                "family": "aromates",
                "picUrl": "WebScrapper.png",
                "waterNeed": "faible" ,
                "careLevel": "facile",
                "growth": "janvier",
                "coldResistance": "fragile",
                "sunNeed": "ombre",
                "heightMature": 30,
                "widthMature": 20
            }

            plant_services.add_plant(attributes)

            return utilities.generate_http_response({"Résultat": "Plante non présente, web-scrapping nécéssaire. \
                Insertion d'une plante par défaut"})

        # Espèce déjà renseignée dans la table informative
        else:
            return utilities.generate_http_response({"plantId": response["records"][0][0]["longValue"]})
        
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
