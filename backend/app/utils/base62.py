import secrets

from fastapi import HTTPException

CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE = 62


def encode(id:int) -> str:

    result = ""

    if id <=0 :
        raise ValueError("ID mush be greater than 0")

    while(id>0):
        idx = (int)(id % BASE)
        result = CHARACTERS[idx] + result
        id = id//62

    return result

def generate_id() -> int:
    id = secrets.randbits(32)
    return id

def decode(code:str) -> int:

    result = 0
    try:
        for ch in code:
            result = result*62 + CHARACTERS.index(ch)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid short code format")

    return result 



    

