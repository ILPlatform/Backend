from Emails import send_email_error
from .VerifyAuth import verify_auth
from firebase_functions import https_fn, options
import json
from Salesforce import getSF
from types import FunctionType
import sys
from functools import wraps
import os

# Custom decorator to allow CORS in the Cloud Function
def https_fn_custom():
    return https_fn.on_request(
    region='europe-west1',
    cors=options.CorsOptions(
        cors_origins="*",
        cors_methods=["get", "post", "options"]
    ))

# Decorator to get the JSON data from the request
def __get_json_data(function):
    @wraps(function)
    def wrapper(request):
        # print(request)
        # print(request.get_json())
        # print(request.get_json(silent=True))
        # data = request.get_json(silent=True).get("data")
        # print(json.loads(request.data.decode('utf8').replace("'", '"')))
        data = json.loads(request.data.decode('utf8').replace("'", '"'))["data"]
        return function(data)
    return wrapper

# Decorator to verify the authentication level
def __auth_verifier(auth_level):
    def decorator(function):
        @wraps(function)
        def wrapper(request):
            message, success = verify_auth(request, auth_level)
            if not success:
                return {"data": {"error": message, "status": 401}}
            return function(request)
        return wrapper
    return decorator

# Decorator to protect the function with a try-except block
def __protect_try_except(function):
    @wraps(function)
    def wrapper(request):
        try:
            return function(request)
        except Exception as e:
            if os.getenv("FUNCTIONS_EMULATOR") == True:
                raise Exception(e)
            else:
                send_email_error(e)
                return {"data": {"error": str(e), "status": 400}}
    return wrapper

# Custom decorator which combines the above decorators
def firebase_functions_custom(auth_level=0):
    def decorator(function):
        @wraps(function)
        def wrapper(request):
            @__auth_verifier(auth_level)
            @__get_json_data
            @__protect_try_except
            def new_function(data):
                return function(data)
            return new_function(request)
        return wrapper
    return decorator
