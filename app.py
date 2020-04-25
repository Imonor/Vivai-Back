"""Main file for Rest API"""
import flask
from flask import Flask

import common.supported_plants as supported_plants
import common.plant_services as plant_services

APP = Flask(__name__)
APP.debug = True

def get_lambda_event_and_context():
    """Converts flask request to amazon lambda's event and context"""
    return {
        "event": flask.request.environ.get("serverless.event"),
        "context": flask.request.environ.get("serverless.context")
        }

@APP.after_request
def after_request_func(response):
    """Adds CORS headers to requests"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = True
    return response

@APP.route("/app/hello")
def hello():
    """Says hello"""
    return {"message": "Hello World!"}

@APP.route("/app/getSupportedPlants", methods=["GET"])
def get_supported_plants():
    """Returns the list of supported plants"""
    env = get_lambda_event_and_context()
    return supported_plants.get_supported_plants(env["event"], env["context"])

@APP.route("/app/insertPlant", methods=["PUT"])
def insertPlant():
    """Insert the plant for linked user"""
    env = get_lambda_event_and_context()
    return plant_services.insert_plant_user(env["event"], env["context"])
    
@APP.route("/app/getListPlants", methods=["GET"])
def get_list_plants_user():
    """Returns all plants for the user"""
    env = get_lambda_event_and_context()
    return plant_services.get_list_plants_user(env["event"], env["context"])

@APP.route("/app/deletePlant", methods=["PUT"])
def delete_user_plant():
    """Deletes the plant for the user"""
    env = get_lambda_event_and_context()
    return plant_services.delete_user_plant(env["event"], env["context"])

@APP.route("/app/updatePlant", methods=["PUT"])
def update_user_plant():
    env = get_lambda_event_and_context()
    return plant_services.update_user_plant(env["event"], env["context"])