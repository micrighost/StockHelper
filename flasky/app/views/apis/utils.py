# google oauth
from google.oauth2 import id_token
from google.auth.transport import requests


def google_log_in(google_token, google_oauth_client_id):
    # google驗證
    try:
        # Specify the GOOGLE_OAUTH2_CLIENT_ID of the app that accesses the backend:
        id_info = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            google_oauth_client_id
        )
    except ValueError:
        # Invalid token
        return None
    return id_info
