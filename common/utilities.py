"""File containing useful functions"""
import json
from botocore.exceptions import ClientError


def generate_http_response(body):
    """Generate a right http response"""
    body = json.dumps(body, ensure_ascii=False).encode('utf8')
    return body

def handle_error(error):
    """Handles the given error"""
    if isinstance(error, ClientError):
        message = {"message": "Error - Unexpected " + error.response.get("Error").get("Code")}
        return generate_http_response(message)
    if isinstance(error, MissingParameterException):
        return generate_http_response(error.response)
    message = {"message": "Error: Unexpected error"}
    return generate_http_response(message)

def get_parameters(event, required_parameters, optionnal_parameters):
    """Returns a dict containing the parameters of the event,
       or raise an error if it doesn't work"""
    parameters = event.get("queryStringParameters")
    if not parameters:
        raise MissingParameterException(required_parameters)

    dict_params = {}
    missing_params = []
    for param in required_parameters:
        value = parameters.get(param)
        if value is None:
            missing_params.append(param)
        else:
            dict_params[param] = value

    if missing_params:
        raise MissingParameterException(missing_params)

    for param in optionnal_parameters:
        value = parameters.get(param, "")
        dict_params[param] = value

    return dict_params

class MissingParameterException(Exception):
    """Exception raised when a required parameter is missing"""
    def __init__(self, missing_parameters):
        super(MissingParameterException, self).__init__()
        self.missing_parameters = missing_parameters
        if len(missing_parameters) == 1:
            self.message = "Parameter " + missing_parameters[0] + " is missing."
        else:
            self.message = "Parameters "
            for param in missing_parameters:
                self.message += param + ", "
            self.message = self.message[:-2] + " are missing."

        self.response = {"message": self.message}
