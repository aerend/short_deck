import enum


class HandRank(enum.IntEnum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    TRIPS = 3
    STRAIGHT = 4
    FULL_HOUSE = 5
    FLUSH = 6
    QUADS = 7
    STRAIGHT_FLUSH = 8


class Suit(enum.IntEnum):
    DIAMONDS = 0
    CLUBS = 1
    HEARTS = 2
    SPADES = 3


class Rank(enum.IntEnum):
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card:
    """Each card is represented as 1 bit in a 52 bit number."""
    def __init__(self, rank=None, suit=None, value=None):
        if value:
            self.value = value
        else:
            self.value = 1 << (rank.value * 4 + suit.value)

    def __repr__(self):
        return f'{self.rank.name} {self.suit.name}'

    @property
    def rank(self):
        return Rank((self.value.bit_length() - 1) >> 2)

    @property
    def suit(self):
        return Suit((self.value.bit_length() - 1) % 4)


class Cards:
    def __init__(self, cards=None, value=None):
        if value:
            self.value = value
        else:
            self.value = 0
            for card in cards:
                self.value |= card.value

    def __repr__(self):
        return str(list(self.cards))

    @property
    def cards(self):
        value = self.value
        while value:
            card_value = value & (~value + 1)
            yield Card(value=card_value)
            value ^= card_value
