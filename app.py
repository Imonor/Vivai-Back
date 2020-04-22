"""Main file for Rest API"""
import flask
from flask import Flask

import common.supported_plant as supported_plant

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

@APP.route("/app/supportedplants", methods=["GET"])
def get_supported_plants():
    """Returns the list of supported plants"""
    env = get_lambda_event_and_context()
    return supported_plant.get_supported_plants(env["event"], env["context"])
