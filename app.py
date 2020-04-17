"""Main file for Rest API"""
import flask
from flask import Flask

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
