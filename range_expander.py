import itertools

from short_deck import poker_types

RANK_STRING_LOOKUP = {
    'a': poker_types.Rank.ACE,
    'k': poker_types.Rank.KING,
    'q': poker_types.Rank.QUEEN,
    'j': poker_types.Rank.JACK,
    't': poker_types.Rank.TEN,
    '9': poker_types.Rank.NINE,
    '8': poker_types.Rank.EIGHT,
    '7': poker_types.Rank.SEVEN,
    '6': poker_types.Rank.SIX,
}

SUIT_STRING_LOOKUP = {
    'd': poker_types.Suit.DIAMONDS,
    'c': poker_types.Suit.CLUBS,
    'h': poker_types.Suit.HEARTS,
    's': poker_types.Suit.SPADES,
}

VALID_RANKS = RANK_STRING_LOOKUP.keys()
VALID_SUITS = SUIT_STRING_LOOKUP.keys()


def single_hand_converter(hand_string):
    """Hands where each card is explicitly given a suit, i.e. AcKd"""
    if len(hand_string) != 4:
        return
    rank_1, suit_1, rank_2, suit_2 = hand_string
    if rank_1 not in VALID_RANKS or rank_2 not in VALID_RANKS:
        return
    if suit_1 not in VALID_SUITS or suit_2 not in VALID_SUITS:
        return
    if rank_1 == rank_2 and suit_1 == suit_2:
        return
    rank_1 = RANK_STRING_LOOKUP[rank_1]
    rank_2 = RANK_STRING_LOOKUP[rank_2]
    suit_1 = SUIT_STRING_LOOKUP[suit_1]
    suit_2 = SUIT_STRING_LOOKUP[suit_2]
    cards = [poker_types.Card(rank_1, suit_1), poker_types.Card(rank_2, suit_2)]
    return [poker_types.Cards(cards=cards)]


def suited_hand_converter(hand_string):
    """Hands that represent all suited pairs of the given ranks, i.e. AKs"""
    if len(hand_string) != 3:
        return
    rank_1, rank_2, s = hand_string
    if s != 's':
        return
    if rank_1 == rank_2:
        return
    rank_1 = RANK_STRING_LOOKUP[rank_1]
    rank_2 = RANK_STRING_LOOKUP[rank_2]
    cards = []
    for suit in poker_types.Suit:
        card_1 = poker_types.Card(rank_1, suit)
        card_2 = poker_types.Card(rank_2, suit)
        cards.append(poker_types.Cards(cards=[card_1, card_2]))
    assert len(cards) == 4
    return cards


def offsuited_handed_converter(hand_string):
    """Hands that represent all offsuited pairs of the given ranks, i.e. AKo"""
    if len(hand_string) != 3:
        return
    rank_1, rank_2, o = hand_string
    if o != 'o':
        return
    rank_1 = RANK_STRING_LOOKUP[rank_1]
    rank_2 = RANK_STRING_LOOKUP[rank_2]
    cards = []
    for suit_1, suit_2 in itertools.permutations(poker_types.Suit, 2):
        card_1 = poker_types.Card(rank_1, suit_1)
        card_2 = poker_types.Card(rank_2, suit_2)
        cards.append(poker_types.Cards(cards=[card_1, card_2]))
    assert len(cards) == 12
    return cards


def paired_hand_converter(hand_string):
    """Hands that represent all possible pairs of the given ranks, i.e. AA"""
    if len(hand_string) != 2:
        return
    rank_1, rank_2 = hand_string
    if rank_1 != rank_2:
        return
    rank_1 = RANK_STRING_LOOKUP[rank_1]
    rank_2 = RANK_STRING_LOOKUP[rank_2]
    cards = []
    for suit_1, suit_2 in itertools.combinations(poker_types.Suit, 2):
        card_1 = poker_types.Card(rank_1, suit_1)
        card_2 = poker_types.Card(rank_2, suit_2)
        cards.append(poker_types.Cards(cards=[card_1, card_2]))
    assert len(cards) == 6
    return cards


def nonpaired_hand_converter(hand_string):
    """Hands that represent all possible combinations that are not pairs, i.e. AK"""
    if len(hand_string) != 2:
        return
    rank_1, rank_2 = hand_string
    if rank_1 == rank_2:
        return
    rank_1 = RANK_STRING_LOOKUP[rank_1]
    rank_2 = RANK_STRING_LOOKUP[rank_2]
    cards = []
    for suit_1 in poker_types.Suit:
        for suit_2 in poker_types.Suit:
            card_1 = poker_types.Card(rank_1, suit_1)
            card_2 = poker_types.Card(rank_2, suit_2)
            cards.append(poker_types.Cards(cards=[card_1, card_2]))
    assert len(cards) == 16
    return cards


CONVERTERS = [
    single_hand_converter,
    suited_hand_converter,
    offsuited_handed_converter,
    paired_hand_converter,
    nonpaired_hand_converter,
]


def expand_range(hand_range_string):
    """Breaks a hand range string into its components 'AA AKs AsQs'"""
    hand_range_string = hand_range_string.lower().strip().split()
    hand_range = set()
    for hand_string in hand_range_string:
        for converter in CONVERTERS:
            hands = converter(hand_string)
            if hands:
                for hand in hands:
                    hand_range.add(hand)
                break
    return hand_range


def expand_board(board_string):
    assert len(board_string) in [0, 2, 4, 6, 8, 10]
    if len(board_string) == 0:
        return 0
    board_string = board_string.lower().strip()
    cards = []
    for i in range(0, len(board_string), 2):
        rank = board_string[i]
        suit = board_string[i + 1]
        assert rank in VALID_RANKS
        assert suit in VALID_SUITS
        cards.append(poker_types.Card(RANK_STRING_LOOKUP[rank], SUIT_STRING_LOOKUP[suit]))
    cards = poker_types.Cards(cards=cards)
    return cards.value
