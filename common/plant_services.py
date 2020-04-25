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

        return utilities.generate_http_response({"Message": "Successfully deleted"})

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)


def insert_plant_user(event, context):
    "Insert plant for the specified user into the database"
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID, PARAM_SPECIES],
                                              [PARAM_PLANT_NICKNAME, PARAM_PLANT_LOCATION, PARAM_PLANT_TEMP,
                                               PARAM_PLANT_SUNEXPO, PARAM_PLANT_SHARED])
        user_id = parameters[PARAM_USER_ID]
        species = parameters[PARAM_SPECIES]

        res = supported_plants.get_plant_id(species)

        
        if ("plantId" in res.keys()):
            plant_id = res["plantId"]
            
            sql_start = f'INSERT INTO {db_dealer.DATABASE}.{db_dealer.USER_PLANT_TABLE} \
                          (userId, plantId'
            sql_end = f'VALUES ("{user_id}", {plant_id}'

            if parameters[PARAM_PLANT_NICKNAME]:
                sql_start += f', {PARAM_PLANT_NICKNAME}'
                sql_end += f', "{parameters[PARAM_PLANT_NICKNAME]}"'
    
            if parameters[PARAM_PLANT_LOCATION]:
                sql_start += f', {PARAM_PLANT_LOCATION}'
                sql_end += f', "{parameters[PARAM_PLANT_LOCATION]}"'
    
            if parameters[PARAM_PLANT_TEMP]:
                sql_start += f', {PARAM_PLANT_TEMP}'
                sql_end += f', {parameters[PARAM_PLANT_TEMP]}'
    
            if parameters[PARAM_PLANT_SUNEXPO]:
                sql_start += f', {PARAM_PLANT_SUNEXPO}'
                sql_end += f', "{parameters[PARAM_PLANT_SUNEXPO]}"'
    
            if parameters[PARAM_PLANT_SHARED]:
                sql_start += f', {PARAM_PLANT_SHARED}'
                sql_end += f', {parameters[PARAM_PLANT_SHARED]}'
    
            sql_statement = sql_start + ') ' + sql_end + ');'
    
            transaction_id = db_dealer.begin_transaction()
            ins = db_dealer.execute_statement_with_id(sql_statement, transaction_id)
            db_dealer.commit_transaction(transaction_id)

            response = {
                "userPlantId": ins["generatedFields"][0]["longValue"],
                "userId": parameters[PARAM_USER_ID],
                "plantId": plant_id
            }
    
            return utilities.generate_http_response(response)
        else:
            return utilities.generate_http_response(res)
        
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

        return utilities.generate_http_response(plants)

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)


def add_plant(attributes):
    """ Adds a new plant in the Plant table ; 
        Returns the request response in case of success, raises an error otherwise"""

    try:
        sql_statement = f'INSERT INTO {db_dealer.DATABASE}.{db_dealer.PLANT_TABLE}({PARAM_SPECIES}, \
                          {PARAM_PIC_URL}, {PARAM_WATER_NEED}, {PARAM_CARE_LEVEL}, {PARAM_GROWTH}, \
                          {PARAM_COLD_RESISTANCE}, {PARAM_SUN_NEED}, {PARAM_HEIGHT_MATURE}, {PARAM_WIDTH_MATURE}'

        if attributes.get(PARAM_FAMILY):
            sql_statement += f', {PARAM_FAMILY}'

        sql_statement += f') VALUES("{attributes[PARAM_SPECIES]}", "{attributes[PARAM_PIC_URL]}", \
                           "{attributes[PARAM_WATER_NEED]}", "{attributes[PARAM_CARE_LEVEL]}", \
                           "{attributes[PARAM_GROWTH]}", "{attributes[PARAM_COLD_RESISTANCE]}", \
                           "{attributes[PARAM_SUN_NEED]}", {attributes[PARAM_HEIGHT_MATURE]}, \
                           {attributes[PARAM_WIDTH_MATURE]}'

        if attributes.get(PARAM_FAMILY):
            sql_statement += f', "{attributes[PARAM_FAMILY]}"'

        sql_statement += f');'

        transaction_id = db_dealer.begin_transaction()
        res_add = db_dealer.execute_statement_with_id(sql_statement, transaction_id)
        db_dealer.commit_transaction(transaction_id)

        return res_add

    except ClientError as error:
        raise error
