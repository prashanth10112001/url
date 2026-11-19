from app.utils.jwt import create_access_token, decode_access_token


def test_create_and_decode_token():
    user_id = 123
    token = create_access_token(user_id)
    payload = decode_access_token(token)

    assert payload["sub"] == str(user_id)

def test_token_is_string():
    user_id = 123
    token = create_access_token(user_id)

    assert isinstance(token,str)

    assert len(token)>0


def test_different_users_get_different_tokens():
    
    token1 = create_access_token(1)
    token2 = create_access_token(2)

    assert token1 != token2



