from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests


class Authenticator:
    CLIENT_ID = ""
    
    def __init__(self, client_id):
        self.CLIENT_ID = client_id

    def authenticate_google(self, request, client_id):
        token = request.get_json()
        token = token["googleToken"]
        
        try:
            profile = id_token.verify_oauth2_token(token,
                                                   googleRequests.Request(),
                                                   client_id)
            print("Authetication was a succes")
            return profile
        except:
            print("failed to authenticate profile")
            return False
        
    def jwt_generator