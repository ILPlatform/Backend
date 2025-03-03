from firebase_admin import auth
from .SafeSF import safe_query
from Salesforce import getSF

# Auth levels:
    # 0 - No authentication required
    # 1 - User authentication required
    # 1.5 - User (curriculum) authenatication required
    # 2 - Admin (replacements) authentication required
    # 3 - Admin (documents) authentication required
    # 4 - Admin (interviews) authentication required
    # 5 - Admin (invoicing) authentication required
    # 10 - Super Admin
def verify_auth(req, auth_level=1):
    if auth_level == 0:
        return "", True
    try:
        authorization = req.headers.get('Authorization')
        token = authorization.split(' ')[1]
        decoded_token = auth.verify_id_token(token, check_revoked=True)
        uid = decoded_token["uid"]

        # Check if the user exists in the database, and attach SF ID if not already attached
        sf = getSF()
        result = safe_query(sf, f"SELECT Id FROM Employee__c WHERE Firebase_UID__c = '{uid}'")
        if len(result) > 0 and not decoded_token.get("sfid"):
            auth.set_custom_user_claims(uid, {"sfid": result[0].get("Id")})

        processed_token = {
            "Id": decoded_token.get("sfid"),
            "Firebase_UID__c": uid,
            "Email__c": decoded_token.get("email"),
            "uid": uid,
            "email": decoded_token["email"],
        }

        if decoded_token.get("roles") and "super_admin" in decoded_token.get("roles"):
            return processed_token, True

        if not decoded_token.get("roles"):
            return f"User {uid} does not have any roles assigned. Please contact an admin for further information.", False

        if auth_level == 1.5 and "no_curriculum" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (curriculum) application. Please contact an admin for further information.", False
        if auth_level == 2 and not "replacements" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (replacements) application. Please contact an admin for further information.", False
        if auth_level == 3 and not "documents" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (documents) application. Please contact an admin for further information.", False
        if auth_level == 4 and not "interviews" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (interviews) application. Please contact an admin for further information.", False
        if auth_level == 10 and not "super_admin" in decoded_token.get("roles"):
            return f"User {uid} does not have access to the (super_admin) application. Please contact an admin for further information.", False

        return processed_token, True
    except Exception as e:
        return f"Could not authenticate user. Error: {e}", False
