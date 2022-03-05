from typing import Union

import utoken
from utoken.exceptions import *


def create_token(payload: dict, key: str) -> str:
    return utoken.encode(payload, key)


def decode_token(token: str, key: str) -> Union[dict, bool]:
    try:
        token_content = utoken.decode(token, key)
    except (
        InvalidContentTokenError,
        ExpiredTokenError,
        InvalidKeyError,
        InvalidTokenError
    ):
        return False
    else:
        return token_content
