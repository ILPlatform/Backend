from firebase_admin import auth

AUTHORIZED_UIDS = {
    # Daniel and Eimantas
    1: ["if4o0vOCGVV62JGgevgQXebtJMI2", "x0YZB7Z0ETUT0HzMscMQ6IrataY2"],
    # Daniel
    2: ["if4o0vOCGVV62JGgevgQXebtJMI2"],
    # No one
    3: []
}

def verify_auth(req, auth_level):
    if auth_level == 0:
        return "", True
    try:
        authorization = req.headers.get('Authorization')
        token = authorization.split(' ')[1]
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
        if uid not in AUTHORIZED_UIDS[auth_level]:
            return f"User {uid} does not have access to the application. Please contact an admin for further information.", False
        return uid, True
    except Exception as e:
        return f"Could not authenticate user. Error: {e}", False
