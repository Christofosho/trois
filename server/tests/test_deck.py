import pytest


@pytest.fixture(scope='module')
def deck():
    from src.deck import Deck
    return Deck()


def test_draw(deck):
    card = deck.draw()
    assert card[0] > -1 and card[0] < 81


def test_check_cards(deck):
    pass


def test_compare_element(deck):
    pass