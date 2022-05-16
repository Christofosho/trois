import pytest


_valid_message_types = set([
    "register",
    "unregister",
    "new_room",
    "join_room",
    "start_room",
    "draw_cards",
    "send_action",
    "end_room",
    "leave_room",
    "heartbeat"
])


@pytest.fixture(scope='module')
def handler():
    from src.handler import Handler
    return Handler()


@pytest.fixture(scope='module')
def user(handler):
    from src.user import User

    class FakeSocket():
        pass

    return User(handler, FakeSocket())


@pytest.fixture(scope='module')
def room(handler):
    from src.room import Room
    return Room(handler)


@pytest.fixture(scope='module')
def validator(handler):
    from src.validator import Validator
    return Validator(handler)


def test_valid_message_types(validator):
    assert validator.valid_message_types == _valid_message_types


def test_validate_message_type(validator):
    assert all(
        validator.validate_message_type(message)
        for message in _valid_message_types
    )


def test_validate_user_id_invalid_None(validator):
    assert validator.validate_user_id(None) is False


def test_validate_user_id_invalid_0(validator):
    assert validator.validate_user_id(0) is False


def test_validate_user_id_valid(validator, user):
    assert validator.validate_user_id(user.user_id) == user


def test_validate_room_id_invalid_None(validator):
    assert validator.validate_room_id(None) is False


def test_validate_room_id_invalid_0(validator):
    assert validator.validate_room_id(0) is False


def test_validate_cards(validator, room):
    room.start()
    cards = [
        # id of each card
        room.active_cards[0][0],
        room.active_cards[1][0],
        room.active_cards[2][0]
    ]
    assert validator.validate_cards(room, cards)
