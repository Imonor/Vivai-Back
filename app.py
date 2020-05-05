"""Main file for Rest API"""
import flask
from flask import Flask
from flask import make_response

import common.supported_plants as supported_plants
import common.plant_services as plant_services
import common.user_plant as user_plant
import common.reporting as reporting

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
    body, status = supported_plants.get_supported_plants(env["event"], env["context"])
    return make_response(body, status)

@APP.route("/app/insertUserPlant", methods=["PUT"])
def insertPlant():
    """Insert the plant for linked user"""
    env = get_lambda_event_and_context()
    body, status = plant_services.insert_user_plant(env["event"], env["context"])
    return make_response(body, status)
    
@APP.route("/app/getListPlants", methods=["GET"])
def get_list_plants_user():
    """Returns all plants for the user"""
    env = get_lambda_event_and_context()
    body, status = plant_services.get_list_plants_user(env["event"], env["context"])
    return make_response(body, status)


@APP.route("/app/deleteUserPlant", methods=["PUT"])
def delete_user_plant():
    """Deletes the plant for the user"""
    env = get_lambda_event_and_context()
    body, status = plant_services.delete_user_plant(env["event"], env["context"])
    return make_response(body, status)

@APP.route("/app/getPlantInfos", methods=["GET"])
def get_plant_infos():
    """Gives infos on plant with PlantId"""
    env = get_lambda_event_and_context()
    body, status = plant_services.get_plant_infos(env["event"], env["context"])
    return make_response(body, status)

@APP.route("/app/getUserPlantInfos", methods=["GET"])
def get_user_plant_infos():
    """Gives infos on a user plant with UserPlantId and UserId"""
    env = get_lambda_event_and_context()
    body, status = user_plant.get_user_plant_infos(env["event"], env["context"])
    return make_response(body, status)

@APP.route("/app/getRandomInfos", methods=["GET"])
def get_plant_anecdotes():
    """Gives random infos on plants""" 
    env = get_lambda_event_and_context()
    body, status = plant_services.get_random_infos(env["event"], env["context"])
    return make_response(body, status)

@APP.route("/app/getSharedPlants", methods=["GET"])
def get_shared_plants():
    """Returns shared plants with specified plantID"""
    env = get_lambda_event_and_context()
    body, status = user_plant.get_shared_plants(env["event"], env["context"])
    return make_response(body, status)

@APP.route("/app/addReporting", methods=["PUT"])
def add_reporting():
    """Adds a reporting in DB"""
    env = get_lambda_event_and_context()
    body, status = reporting.add_reporting(env["event"], env["context"])
    return make_response(body, status)

@APP.route("/app/getReportings", methods=["GET"])
def get_reportings():
    """Returns the 7 last reportings for a given userPlant"""
    env = get_lambda_event_and_context()
    body, status = reporting.get_reportings(env["event"], env["context"])
    return make_response(body, status)
    
@APP.route("/app/updatePlant", methods=["PUT"])
def update_plant():
    """Updates plant object with userPlantId"""
    env = get_lambda_event_and_context()
    body, status = plant_services.update_plant(env["event"], env["context"])
    return make_response(body, status)
