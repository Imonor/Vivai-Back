"""File containing all the functions to deal with the database"""

from uuid import uuid4
import boto3
from botocore.exceptions import ClientError

DYNAMODB_CLIENT = boto3.client('dynamodb', 'eu-west-1')

# Table's Name
SUPPORTED_PLANT_TABLE = "SupportedPlant"
PLANT_TABLE = "Plant"
USER_PLANT_TABLE = "UserPlant"
PLANT_TABLE = "Plant"

def get_all_items(table):
    """Returns all items from a table"""
    try:
        response = DYNAMODB_CLIENT.scan(TableName=table, Select='ALL_ATTRIBUTES', Limit=5)
        return response["Items"]
    except ClientError as error:
        raise error

def insert_item(table, params):
    """Inserts an item in the given table, using the parameters.
       Returns the generated UUID"""
    try:
        item_id = str(uuid4())
        item = {"id": {"S": item_id}}

        for param in params:
            if params[param] is None:
                item[param] = {"NULL": True}

            elif isinstance(params[param], str):
                item[param] = {"S": params[param]}

            elif isinstance(params[param], bool):
                item[param] = {"BOOL": params[param]}
            else:
                item[param] = {"N": str(params[param])}

        DYNAMODB_CLIENT.put_item(TableName=table, Item=item)
        return item_id

    except ClientError as error:
        raise error
