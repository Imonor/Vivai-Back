"File for Plant Services"

from botocore.exceptions import ClientError

import common.utilities as utilities
import common.db_dealer as db_dealer

import common.supported_plants as supported_plants

PARAM_USER_ID = "userId"
PARAM_PLANT_ID = "plantId"
PARAM_PLANT_LOCATION = "location"
PARAM_PLANT_TEMP = "temperature"
PARAM_PLANT_SUNEXPO = "sunExpo"
PARAM_PLANT_SHARED = "shared"
PARAM_PLANT_NICKNAME = "nickname"

PARAM_SPECIES = "species"
PARAM_FAMILY = "family"
PARAM_PIC_URL = "picUrl"
PARAM_WATER_NEED = "waterNeed"
PARAM_CARE_LEVEL = "careLevel"
PARAM_GROWTH = "growth"
PARAM_COLD_RESISTANCE = "coldResistance"
PARAM_SUN_NEED = "sunNeed"
PARAM_HEIGHT_MATURE = "heightMature"
PARAM_WIDTH_MATURE = "widthMature"

PARAM_USER_PLANT_ID = "userPlantId"

def delete_user_plant(event, context):
    "Delete plant at the specified user plant ID"

    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_PLANT_ID], [])
        user_plant_id = parameters[PARAM_USER_PLANT_ID]

        sql_statement = f'DELETE FROM {db_dealer.DATABASE}.{db_dealer.USER_PLANT_TABLE} \
            WHERE id = {user_plant_id};'

        transaction_id = db_dealer.begin_transaction()
        db_dealer.execute_statement_with_id(sql_statement, transaction_id)
        db_dealer.commit_transaction(transaction_id)

        return utilities.generate_http_response({"Message": "Successfully deleted"}), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)


def insert_user_plant(event, context):
    "Insert plant for the specified user into the database"
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID, PARAM_SPECIES],
                                              [PARAM_PLANT_NICKNAME, PARAM_PLANT_LOCATION, PARAM_PLANT_TEMP,
                                               PARAM_PLANT_SUNEXPO, PARAM_PLANT_SHARED])
        species = parameters[PARAM_SPECIES]

        plant_id = supported_plants.get_plant_id(species)

        
        if plant_id:

            if not parameters[PARAM_PLANT_NICKNAME]:
                parameters[PARAM_PLANT_NICKNAME] = None
    
            if not parameters[PARAM_PLANT_LOCATION]:
                parameters[PARAM_PLANT_LOCATION] = None
    
            if not parameters[PARAM_PLANT_TEMP]:
                parameters[PARAM_PLANT_TEMP] = None
    
            if not parameters[PARAM_PLANT_SUNEXPO]:
                parameters[PARAM_PLANT_SUNEXPO] = None
    
            if not parameters[PARAM_PLANT_SHARED]:
                parameters[PARAM_PLANT_SHARED] = False

            user_plant_id = db_dealer.insert_item(db_dealer.USER_PLANT_TABLE, parameters)

            response = {
                "userPlantId": user_plant_id,
                "plantId": plant_id
            }
    
            return utilities.generate_http_response(response), 200
        
        return utilities.generate_http_response({"Message": "Web-scrapping nécessaire"}), 501
        
    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)

def get_list_plants_user(event, context):
    "Get list of plants for the specified user"
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID], [])

        user_id = parameters[PARAM_USER_ID]

        sql_statement = f'SELECT uplant.id, plantId, userId, nickname, location, temperature, sunExpo, shared, plant.picUrl \
                          FROM {db_dealer.DATABASE}.{db_dealer.USER_PLANT_TABLE} as uplant JOIN \
                          {db_dealer.DATABASE}.{db_dealer.PLANT_TABLE} as plant ON uplant.plantId = plant.id \
                          WHERE uplant.userID = "{user_id}"'

        response = db_dealer.execute_statement(sql_statement)

        plants = []
        for record in response['records']:
            plant = {
                "id": record[0]["longValue"],
                "plantId": record[1]["longValue"],
                "userId": record[2]["stringValue"],
                "nickname": "NULL" if "isNull" in record[3] else record[3]["stringValue"],
                "location": "NULL" if "isNull" in record[4] else record[4]["stringValue"],
                "temperature": "NULL" if "isNull" in record[5] else record[5]["stringValue"],
                "sunExpo": "NULL" if "isNull" in record[6] else record[6]["stringValue"],
                "shared": record[7]["booleanValue"],
                "picUrl": record[8]["stringValue"]
            }
            plants.append(plant)

        return utilities.generate_http_response(plants), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)


def add_plant(attributes):
    """ Adds a new plant in the Plant table ; 
        Returns the request response in case of success, raises an error otherwise"""

    try:
        if PARAM_FAMILY not in attributes:
            attributes[PARAM_FAMILY] = None

        plant_id = db_dealer.insert_item(db_dealer.PLANT_TABLE, attributes)

        return plant_id

    except ClientError as error:
        raise error
