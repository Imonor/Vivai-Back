"""File for Plant Services"""

import random

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
PARAM_USER_PLANT_ID = "userPlantId"

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

def get_plant_anecdotes(event, context):
    try:
        lines = open('anecdotes.txt').read().splitlines()
        line = random.choice(lines)
        return utilities.generate_http_response(line)

    except ClientError as error:
        raise error

def delete_user_plant(event, context):
    """Delete plant at the specified user plant ID"""

    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID, PARAM_USER_PLANT_ID], [])
        user_id = parameters[PARAM_USER_ID]
        user_plant_id = parameters[PARAM_USER_PLANT_ID]

        db_dealer.delete_item(db_dealer.USER_PLANT_TABLE, user_plant_id, "userId", user_id)

        return utilities.generate_http_response({"Message": "Successfully deleted"}), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)

def get_plant_infos(event, context):
    """Gives infos on plant with plantId"""
    try:
        parameters = utilities.get_parameters(event, [PARAM_PLANT_ID], [])
        plant_id = parameters[PARAM_PLANT_ID]

        item = db_dealer.get_item(db_dealer.PLANT_TABLE, plant_id, "", "", [])

        response = {
            "careLevel": item["careLevel"]["S"],
            "coldResistance": item["coldResistance"]["S"],
            "family": item["family"]["S"],
            "growth": item["growth"]["S"],
            "heightMature": item["heightMature"]["S"],
            "picUrl": item["picUrl"]["S"],
            "species": item["species"]["S"],
            "sunNeed": item["sunNeed"]["S"],
            "waterNeed": item["waterNeed"]["S"],
            "widthMature": item["widthMature"]["S"]
        }

        return utilities.generate_http_response(response), 200
    
    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)

def insert_user_plant(event, context):
    "Insert plant for the specified user into the database"
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID, PARAM_SPECIES],
                                              [PARAM_PLANT_NICKNAME, PARAM_PLANT_LOCATION, PARAM_PLANT_TEMP,
                                               PARAM_PLANT_SUNEXPO, PARAM_PLANT_SHARED])
        species = parameters[PARAM_SPECIES]

        plant_id, picUrl = supported_plants.get_plant_infos(species)

        
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

            parameters["plantId"] = plant_id
            parameters["picUrl"] = picUrl

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
        items = db_dealer.list_items(db_dealer.USER_PLANT_TABLE, "userId", user_id)

        plants = []
        for item in items:
            plant = {
                "id": item["id"]["S"],
                "plantId": item["plantId"]["S"],
                "userId": item["userId"]["S"],
                "nickname": "NULL" if "NULL" in item["nickname"] else item["nickname"]["S"],
                "location": "NULL" if "NULL" in item["location"] else item["location"]["S"],
                "temperature": "NULL" if "NULL" in item["temperature"] else item["temperature"]["S"],
                "sunExpo": "NULL" if "NULL" in item["sunExpo"] else item["sunExpo"]["S"],
                "shared": item["shared"]["BOOL"],
                "picUrl": item["picUrl"]["S"],
                "species": item["species"]["S"]
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
