import pytest


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


def test_reset(room):
    room.reset()
    assert (
        len(room.deck.current) == 81
        and room.game_stage == 0
        and room.active_cards == []
        and room.started is False
        and room.start_room == set()
        and room.draw_cards == set()
        and room.end_room == set()
    )


def test_add_user(room, user):
    room.add_user(user)
    assert len(room.players) == 1


def test_get_user(room, user):
    assert user.user_id in room.get_users()


def test_start(room):
    room.start()
    assert (
        room.game_stage == 1
        and len(room.active_cards) == 12
        and not room.start_room
        and not room.draw_cards
        and not room.end_room
        and room.started is True
        and all(user.score == 0 for user in room.players.values())
    )


def test_add_cards_success(room):
    assert room.add_cards() is True


def test_remove_cards(room):
    assert room.remove_cards() is None


def test_get_public_information(room):
    pass
