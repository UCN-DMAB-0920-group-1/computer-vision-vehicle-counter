import jwt
from google.oauth2 import id_token
from google.auth.transport import requests as googleRequests
import requests


class Authenticator:

    def __init__(self, client_id, secret_key, algorithm, client_secret):
        self.CLIENT_ID = client_id
        self.SECRET_KEY = secret_key
        self.ALGORITHM = algorithm
        self.CLIENT_SECRET = client_secret

    def authenticate_google(self, code):

        data = {
            'code': code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "redirect_uri": "http://localhost:8080",
            "grant_type": "authorization_code"
        }

        try:
            _google_res = requests.post("https://oauth2.googleapis.com/token",
                                        data=data)
            _google_res = _google_res.json()
            _id_token = _google_res["id_token"]

            _profile = id_token.verify_oauth2_token(_id_token,
                                                    googleRequests.Request(),
                                                    self.CLIENT_ID)
            _payload = {
                "exp": _profile["exp"],
                "name": _profile["name"],
                "picture": _profile["picture"],
                "valid": "True",
                "UUID": _profile["sub"]
            }

            _token = self.JWT_creation(_payload)
            return _token
        except Exception as e:
            print("failed to authenticate profile: " + str(e))
            return ""

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
            return True if _token["valid"] == "True" else False
        except Exception as e:
            print("JWT token was not valid: " + str(e))
            return False

    def checkPermission(self, request):
        res = False
        if "Authorization" in request.headers:
            # decoes JWT and looks at payload value "valid" return true if succes and false if not
            res = self.authenticate_JWT(request.headers["Authorization"])
        return res
