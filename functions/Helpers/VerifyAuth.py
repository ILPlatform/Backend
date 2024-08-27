from firebase_admin import auth

# Auth levels:
    # 0 - No authentication required
    # 1 - User authentication required
    # 2 - Admin (replacements) authentication required
    # 3 - Admin (documents) authentication required
    # 4 - Admin (interviews) authentication required
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
        if auth_level == 4 and not "interviews" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (interviews) application. Please contact an admin for further information.", False
        if auth_level == 10 and not "super_admin" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (super_admin) application. Please contact an admin for further information.", False

        return {"uid": uid, "email": decoded_token["email"]}, True
    except Exception as e:
        return f"Could not authenticate user. Error: {e}", False
