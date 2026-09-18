from pydantic import Basemodel

class Token(Basemodel):
    access_token: str
    token_type: str = "bearer"

class TokenData(Basemodel):
    username: str |None=None

