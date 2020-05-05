"""File containing services for Supported Plants"""

from datetime import date, datetime

from botocore.exceptions import ClientError

import common.utilities as utilities
import common.db_dealer as db_dealer

PARAM_USER_PLANT_ID = "userPlantId"
PARAM_WATER = "water"
PARAM_PRUNE = "prune"
PARAM_REPOTTING = "repotting"
PARAM_HARVEST = "harvest"
PARAM_COMMENT = "comment"

def add_reporting(event, context):
    """Adds a reporting in the database"""
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_PLANT_ID], [PARAM_WATER, PARAM_PRUNE, PARAM_REPOTTING,
                                                                            PARAM_HARVEST, PARAM_COMMENT])
        parameters["date"] = str(date.today())
    
        parameters[PARAM_WATER] = (parameters[PARAM_WATER].lower() == "true")
        parameters[PARAM_PRUNE] = (parameters[PARAM_PRUNE].lower() == "true")
        parameters[PARAM_REPOTTING] = (parameters[PARAM_REPOTTING].lower() == "true")
        parameters[PARAM_HARVEST] = (parameters[PARAM_HARVEST].lower() == "true")
    
        if not parameters[PARAM_COMMENT]:
            parameters[PARAM_COMMENT] = None
    
        db_dealer.insert_item(db_dealer.REPORTING_TABLE, parameters)
        return utilities.generate_http_response({"Message": "Success"}), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)

def get_reportings(event, context):
    """Returns the 7 last reportings for a given userPlant"""
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_PLANT_ID], [])
        user_plant_id = parameters[PARAM_USER_PLANT_ID]
    
        items = db_dealer.list_items(db_dealer.REPORTING_TABLE,"userPlantId", user_plant_id)
        items.sort(reverse=True, key=lambda dict: datetime.strptime(dict["date"]["S"], "%Y-%m-%d"))

        if len(items) > 7:
            items = items[:7]

        reports = []
        for item in items:
            report = {
                "date": item["date"]["S"],
                "water": item["water"]["BOOL"],
                "prune": item["prune"]["BOOL"],
                "repotting": item["repotting"]["BOOL"],
                "harvest": item["harvest"]["BOOL"],
                "comment": "NULL" if "NULL" in item["comment"] else item["comment"]["S"]
            }
            reports.append(report)

        return utilities.generate_http_response(reports), 200

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)