from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests


class Authenticator:
    CLIENT_ID = '512124053214-vpk9p42i9ls413asejsa9bg7j1b4nq61.apps.googleusercontent.com'

    def authenticate(self, request):
        token = request["googleToken"]
        try:
            profile = id_token.verify_oauth2_token(token,
                                                   googleRequests.Request(),
                                                   self.CLIENT_ID)
            print("Authetication was a succes")
            return profile
        except:
            print("failed to authenticate profile")
            return False