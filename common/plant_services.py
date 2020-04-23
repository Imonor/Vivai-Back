"File for Plant Services"

from botocore.exceptions import ClientError

import common.utilities as utilities
import common.db_dealer as db_dealer

PARAM_USER_ID = "userId"
PARAM_PLANT_ID = "plantId"
PARAM_PLANT_LOCATION = "location"
PARAM_PLANT_TEMP = "temperature"
PARAM_PLANT_SUNEXPO = "sunExpo"
PARAM_PLANT_SHARED = "shared"

def insert_plant_user(event, context):
    "Insert plant for the specified user into the database"
    try:
        parameters = utilities.get_parameters(event, [PARAM_USER_ID, PARAM_PLANT_ID],
                                              [PARAM_PLANT_LOCATION, PARAM_PLANT_TEMP,
                                               PARAM_PLANT_SUNEXPO, PARAM_PLANT_SHARED])
        user_id = parameters[PARAM_USER_ID]
        plant_id = parameters[PARAM_PLANT_ID]

        sql_start = f'INSERT INTO {db_dealer.DATABASE}.{db_dealer.USER_PLANT_TABLE} \
                      (userId, plantId'
        sql_end = f'VALUES ("{user_id}", {plant_id}'

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
        db_dealer.execute_statement_with_id(sql_statement, transaction_id)
        db_dealer.commit_transaction(transaction_id)

        return utilities.generate_http_response({"message": "Success"})

    except (ClientError, utilities.MissingParameterException) as error:
        return utilities.handle_error(error)
