def test_to_json_utf8_empty():
    from src.message import Message
    message = Message()
    assert message.to_json_utf8() == b'{}'
