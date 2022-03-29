from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests
import jwt


class Authenticator:

    def __init__(self, client_id, secret_key, algorithm):
        self.CLIENT_ID = client_id
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm

    def authenticate_google(self, request):
        _token = request.get_json()
        _token = _token["googleToken"]

        try:
            _profile = id_token.verify_oauth2_token(_token,
                                                    googleRequests.Request(),
                                                    self.CLIENT_ID)
            _payload = {
                "exp": _profile["exp"],
                "name": _profile["name"],
                "picture": _profile["picture"],
                "valid": "True"
            }

            _token = self.JWT_creation(_payload)
            return _token
        except:
            print("failed to authenticate profile")
            return False

    def JWT_creation(self, profile):
        user_jwt = jwt.encode(payload=profile,
                              key=self.SECRET_KEY,
                              algorithm=self.ALGORITHM)
        return user_jwt

    def authenticate_JWT(self, token):
        try:
            _token = jwt.decode(jwt=token,
                                key=self.SECRET_KEY,
                                algorithms=[self.ALGORITHM])
            print(_token)
            return True
        except jwt.exceptions.InvalidTokenError:
            return False
