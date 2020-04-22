"""File containing services for Supported Plants"""

from botocore.exceptions import ClientError
import common.db_dealer as db_dealer
import common.utilities as utilities

PARAM_SEARCH = "search"

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
