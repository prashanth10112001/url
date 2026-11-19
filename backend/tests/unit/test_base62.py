from app.utils.base62 import decode, encode

def test_encode_decode_roundtrip():

    original_id = 12345

    short_code = encode(original_id)

    decoded_id = decode(short_code)

    assert decoded_id == original_id

def test_encode_decode_roundtrip_multiple_ids():

    ids = [
            1,
            10,
            100,
            999,
            12345,
            9999999
    ]

    for original_id in ids:

        shortcode = encode(original_id)

        decoded_id = decode(shortcode)

        assert decoded_id == original_id


def test_encode_returns_string():

    short_code = encode(1)

    assert isinstance(
        short_code,
        str
    )

    assert len(short_code) > 0