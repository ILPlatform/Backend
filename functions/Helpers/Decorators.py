from Emails import send_email_error
from .VerifyAuth import verify_auth
from firebase_functions import https_fn, options
import json
from Salesforce import getSF
from types import FunctionType
import sys
from functools import wraps
import os
import re

# Custom decorator to allow CORS in the Cloud Function
def https_fn_custom(timeout_sec=60, memory=256, access=False):
    if os.getenv("FUNCTIONS_EMULATOR") == "true":
        return https_fn.on_request(
        region='europe-west1',
        cors=options.CorsOptions(
            cors_origins=["*"],
            cors_methods=["get", "post", "options"]
        ),
        timeout_sec=timeout_sec,
        memory=memory)
    else:
        return https_fn.on_request(
        region='europe-west1',
        cors=options.CorsOptions(
            cors_origins=[
                "https://www.ilplatform.be",
                "https://admin.ilplatform.be",
                "https://curriculum.ilplatform.be",
                "https://independentlearningplatform.lightning.force.com",
                "https://independentlearningplatform--internbox.sandbox.lightning.force.com"
            ],
            cors_methods=["get", "post", "options"]
        ),
        timeout_sec=timeout_sec)

# Decorator to get the JSON data from the request
def __get_json_data(function):
    @wraps(function)
    def wrapper(request):
        data = json.loads(request.data.decode('utf8').replace("'", '"')).get("data", {}) or {}

        # Add the uid to the data
        user_details, logged_in = verify_auth(request)
        if logged_in:
            data["user_details"] = user_details
            data["uid"] = user_details.get("uid")
            data["user_email"] = user_details.get("email")
            data["admin_role"] = user_details.get("admin_role")

        return function(data)
    return wrapper

# Decorator to verify the authentication level
def __auth_verifier(auth_level):
    def decorator(function):
        @wraps(function)
        def wrapper(request):
            message, success = verify_auth(request, auth_level)
            if not success:
                return {"data": {"error": message, "status": 401}}, 401
            return function(request)
        return wrapper
    return decorator

# Decorator to protect the function with a try-except block
def __protect_try_except(function):
    @wraps(function)
    def wrapper(request):
        try:
            return function(request), 200
        except Exception as e:
            # if os.getenv("FUNCTIONS_EMULATOR") == "true":
            #     raise Exception(e)
            # else:
            #     send_email_error(e)
            return {"data": {"error": str(e), "status": 400}}, 400
        if request.environ.get("werkzeug.server.shutdown") or request.stream.closed:
            print("Request was aborted by the client.")
            return {"status": 499, "error": "Request Aborted"}, 499
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
