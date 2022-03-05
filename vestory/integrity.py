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


def decode_tokens(tokens: list, key: str) -> list:
    """Decode a list of tokens.

    If any element of this list
    is False, it means that the token is not
    can be decoded.

    :param tokens: List of tokens.
    :type tokens: list
    :param key: Key to decode
    :type key: str
    :return: Returns a list of decoded tokens.
    :rtype: list
    """

    decoded_tokens = []
    for t in tokens:
        content = decode_token(t, key)
        decode_token.append(content)
    
    return decoded_tokens


def decode_without_key(token: str) -> dict:
    """Decodifica um token
    sem a necessidade da chave.

    Sem a chave, é impossível
    garantir a integridade.

    :param token: Token 
    :type token: str
    :return: Conteúdo do token
    :rtype: dict
    """

    try:
        token_content = utoken.decode_without_key(token)
    except (
        InvalidContentTokenError,
        ExpiredTokenError,
        InvalidTokenError
    ):
        return False
    else:
        return token_content
