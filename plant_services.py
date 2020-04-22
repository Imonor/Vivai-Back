"File for Plant Services"

from botocore.exceptions import ClientError

import common.utilities as utilities
import common.db_dealer as db_dealer

PARAM_USER_ID = "userId"
PARAM_PLANT_ID = "plantId"

def insert_plant_user(event, context):
    "Insert plant for the specified user into the database"
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID, PARAM_PLANT_ID], [])
        user_id = parameters[PARAM_USER_ID]
        plant_id = parameters[PARAM_PLANT_ID]

        trans_id = db_dealer.begin_transaction()
        sql_statement = f"INSERT INTO {db_dealer.DATABASE}.{db_dealer.USER_PLANT_TABLE} \
                          (plantId, userId) \
                          VALUES ({plant_id}, {user_id});"
        response = db_dealer.execute_statement_with_id(sql_statement, trans_id)
        updated = response['numberOfRecordsUpdated']
        db_dealer.commit_transaction(trans_id)

        return utilities.generate_http_response(updated)

    except (ClientError, utilities.MissingParameterException) as error:
        return (utilities.handle_error(error))
