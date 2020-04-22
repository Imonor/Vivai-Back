"""File containing all the functions to deal with the database"""

import os
import boto3
from botocore.exceptions import ClientError

RDS_DATA_CLIENT = boto3.client('rds-data', 'eu-west-1')
DATABASE = "Vivai"

# Tables' Name
SUPPORTED_PLANT_TABLE = "SupportedPlant"

RESOURCE_ARN = os.getenv("RESOURCE_ARN")
SECRET_ARN = os.getenv("SECRET_ARN")

def begin_transaction():
    """Begins a transaction and return its id"""
    try:
        transaction = RDS_DATA_CLIENT.begin_transaction(database=DATABASE,
                                                        resourceArn=RESOURCE_ARN,
                                                        secretArn=SECRET_ARN)
        return transaction["transactoinId"]
    except ClientError as error:
        raise error

def commit_transaction(transaction_id):
    """Commits a transaction on the database"""
    try:
        RDS_DATA_CLIENT.commit_transaction(resourceArn=RESOURCE_ARN,
                                           secretArn=SECRET_ARN,
                                           transactionId=transaction_id)
    except ClientError as error:
        raise error

def rollback_transaction(transaction_id):
    """Rollbacks a transaction on the database"""
    try:
        RDS_DATA_CLIENT.rollback_transaction(resourceArn=RESOURCE_ARN,
                                             secretArn=SECRET_ARN,
                                             transactionId=transaction_id)
    except ClientError as error:
        raise error

def execute_statement(sql_statement):
    """Executes the SQL statement on the database"""
    try:
        response = RDS_DATA_CLIENT.execute_statement(database=DATABASE,
                                                     resourceArn=RESOURCE_ARN,
                                                     secretArn=SECRET_ARN,
                                                     sql=sql_statement)
        return response
    except ClientError as error:
        raise error

def execute_statement_with_id(sql_statement, transaction_id):
    """Executes the SQL statement on the database"""
    try:
        response = RDS_DATA_CLIENT.execute_statement(transactionId=transaction_id,
                                                     database=DATABASE,
                                                     resourceArn=RESOURCE_ARN,
                                                     secretArn=SECRET_ARN,
                                                     sql=sql_statement)
        return response
    except ClientError as error:
        raise error
