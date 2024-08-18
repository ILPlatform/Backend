from firebase_admin import auth

AUTHORIZED_UIDS = {
    # Daniel and Eimantas and bot
    1: ["if4o0vOCGVV62JGgevgQXebtJMI2", "x0YZB7Z0ETUT0HzMscMQ6IrataY2", "v2IRZ16j6zcxAKObK1y1T7lFTaR2"],
    # Daniel and bot
    2: ["if4o0vOCGVV62JGgevgQXebtJMI2", "v2IRZ16j6zcxAKObK1y1T7lFTaR2"],
    # No one
    3: []
}

# Auth levels:
    # 0 - No authentication required
    # 1 - User authentication required
    # 2 - Admin (replacements) authentication required
    # 3 - Admin (documents) authentication required
    # 10 - Super Admin
def verify_auth(req, auth_level=1):
    if auth_level == 0:
        return "", True
    try:
        authorization = req.headers.get('Authorization')
        token = authorization.split(' ')[1]
        decoded_token = auth.verify_id_token(token, check_revoked=True)
        uid = decoded_token["uid"]

        if auth_level == 2 and not "replacements" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (replacements) application. Please contact an admin for further information.", False
        if auth_level == 3 and not "documents" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (documents) application. Please contact an admin for further information.", False
        if auth_level == 10 and not "super_admin" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (super_admin) application. Please contact an admin for further information.", False

        return {"uid": uid, "email": decoded_token["email"]}, True
    except Exception as e:
        return f"Could not authenticate user. Error: {e}", False
