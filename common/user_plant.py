"""File containing services for UserPlant"""

from datetime import date
from botocore.exceptions import ClientError

import common.utilities as utilities
import common.db_dealer as db_dealer

PARAM_USER_ID = "userId"
PARAM_USER_PLANT_ID = "userPlantId"
PARAM_PLANT_ID = "plantId"

def get_notifications(event, context):
    """Returns notification for reporting"""
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID], [])
        user_id = parameters[PARAM_USER_ID]
        items = db_dealer.list_items(db_dealer.USER_PLANT_TABLE, "userId", user_id)
        notifs = []
        for item in items:
            report_item = db_dealer.get_item(db_dealer.REPORTING_TABLE, item["userPlantId"]["S"], "date", date.today(), [])
            if not report_item:
                notifs.append(item["species"]["S"])
        return utilities.generate_http_response(notifs), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)


def get_shared_plants(event, context):
    """Returns shared plants of given plantID"""
    try:
        parameters = utilities.get_parameters(event, [PARAM_PLANT_ID, PARAM_USER_ID], [])
        plant_id = parameters[PARAM_PLANT_ID]
        user_id = parameters[PARAM_USER_ID]
        items = db_dealer.get_all_items(db_dealer.USER_PLANT_TABLE)

        plants = []
        for item in items:
            if item["plantId"]["S"] == plant_id and item["shared"]["BOOL"] and item["userId"]["S"] != user_id:
                plant = {
                    "id": item["id"]["S"],
                    "picUrl": item["picUrl"]["S"],
                    "plantId": item["plantId"]["S"],
                    "userId": item["userId"]["S"],
                    "nickname": "NULL" if "NULL" in item["nickname"] else item["nickname"]["S"],
                    "location": "NULL" if "NULL" in item["location"] else item["location"]["S"],
                    "temperature": "NULL" if "NULL" in item["temperature"] else item["temperature"]["S"],
                    "sunExpo": "NULL" if "NULL" in item["sunExpo"] else item["sunExpo"]["S"],
                    "species": item["species"]["S"]
                }
                plants.append(plant)

        return utilities.generate_http_response(plants), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)


def get_user_plant_infos(event, context):
    """Returns the infos of a user's plant"""
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID, PARAM_USER_PLANT_ID], [])
        user_id = parameters[PARAM_USER_ID]
        user_plant_id = parameters[PARAM_USER_PLANT_ID]

        item = db_dealer.get_item(db_dealer.USER_PLANT_TABLE, user_plant_id, "userId", user_id, [])

        user_plant ={
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
        return utilities.generate_http_response(user_plant), 200

    except ClientError as error:
        return utilities.handle_error(error)
