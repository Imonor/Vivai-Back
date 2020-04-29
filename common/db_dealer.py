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

def get_attributes(table, attributes, condition_param, condition_op, condition_value):
    """Returns the wanted attributes for the first item that match the condition.
       Parameter condition is a string describing the condition e.g. "species = 'basilic'"
    """
    condition = condition_param + " " + condition_op + " :val"

    if isinstance(condition_value, str):
        expr_attr_value = {":val": {"S": condition_value}}

    elif isinstance(condition_value, bool):
        expr_attr_value = {":val": {"BOOL": condition_value}}

    else:
        expr_attr_value = {":val": {"N": str(condition_value)}}

    try: 
        response = DYNAMODB_CLIENT.scan(TableName=table, Select="SPECIFIC_ATTRIBUTES", Limit=1,
                                        ProjectionExpression=", ".join(attributes), FilterExpression=condition,
                                        ExpressionAttributeValues=expr_attr_value)
        if response["Items"]:
            return response["Items"][0]
        return None
    except ClientError as error:
        raise error

def list_items(table, key_param, key_value):
    """Returns all the items that match the given sort key"""
    
    condition = key_param + " = :val"
    expr_attr_value = {":val": {"S": key_value}}

    response = DYNAMODB_CLIENT.query(TableName=table, KeyConditionExpression=condition, 
                                     ExpressionAttributeValues=expr_attr_value)

    return response["Items"]
