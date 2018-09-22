import itertools

from poker_types import Rank
import poker_types
import card_generators

SEVEN_CARD = 'seven_card_strength_lookup_table'
FIVE_CARD = 'five_card_strength_lookup_table'

# TODO: some unecessary sorting is done


def _is_quads(cards):
    ranks = [card.rank for card in cards]
    for rank in ranks:
        if ranks.count(rank) == 4:
            return [rank] + [r for r in ranks if r != rank]
    return False


def _is_flush(cards):
    suits = [card.suit for card in cards]
    if suits.count(suits[0]) == 5:
        return sorted((card.rank for card in cards), reverse=True)
    return False


def _is_straight(cards):
    ranks = sorted((card.rank for card in cards))
    if ranks == [Rank.SIX, Rank.SEVEN, Rank.EIGHT, Rank.NINE, Rank.ACE]:
        return [Rank.NINE]
    no_duplicates = len(set(ranks)) == 5
    sequential = ranks[4].value - ranks[0].value == 4
    if no_duplicates and sequential:
        return [ranks[4]]
    return False


def _is_straight_flush(cards):
    high = _is_straight(cards)
    if high and _is_flush(cards):
        return high
    return False


def _is_trips(cards):
    ranks = [card.rank for card in cards]
    for rank in ranks:
        if ranks.count(rank) == 3:
            return [rank] + sorted((r for r in ranks if r != rank), reverse=True)
    return False


def _is_pair(cards):
    ranks = [card.rank for card in cards]
    for rank in ranks:
        if ranks.count(rank) == 2:
            return [rank] + sorted((r for r in ranks if r != rank), reverse=True)
    return False


def _is_full_house(cards):
    trips = _is_trips(cards)
    pair = _is_pair(cards)
    if trips and pair:
        return trips[:1] + pair[:1]
    return False


def _is_two_pair(cards):
    pair_1 = _is_pair(cards)
    if pair_1:
        remaining_cards = [card for card in cards if card.rank != pair_1[0]]
        pair_2 = _is_pair(remaining_cards)
        if pair_2:
            return pair_1[:1] + pair_2[:1] + [card.rank for card in remaining_cards if card.rank != pair_2[0]]
    return False


def _is_high_card(cards):
    return sorted((card.rank for card in cards), reverse=True)


EVALUATORS = {
    poker_types.HandRank.STRAIGHT_FLUSH: _is_straight_flush,
    poker_types.HandRank.QUADS: _is_quads,
    poker_types.HandRank.FLUSH: _is_flush,
    poker_types.HandRank.FULL_HOUSE: _is_full_house,
    poker_types.HandRank.TRIPS: _is_trips,
    poker_types.HandRank.STRAIGHT: _is_straight,
    poker_types.HandRank.TWO_PAIR: _is_two_pair,
    poker_types.HandRank.PAIR: _is_pair,
    poker_types.HandRank.HIGH_CARD: _is_high_card
}


def get_hand_strength(cards):
    cards = sorted(cards.cards, reverse=True, key=lambda x: x.value)
    for hand, evaluator in EVALUATORS.items():
        ranks = evaluator(cards)
        if not ranks:
            continue
        strength = hand.value
        for rank_index in range(5):
            strength = strength << 4
            if rank_index < len(ranks):
                strength += ranks[rank_index].value
        return strength


def build_five_card_strength_lookup_table():
    lookup_table = {}
    for card_value in card_generators.generate_all_card_combinations(5):
        cards = poker_types.Cards(value=card_value)
        lookup_table[card_value] = get_hand_strength(cards)
    return lookup_table


def build_seven_card_strength_lookup_table():
    lookup_table = {}
    five_card_strength_lookup_table = build_five_card_strength_lookup_table()
    for card_value in card_generators.generate_all_card_combinations(7):
        cards = poker_types.Cards(value=card_value).cards
        best_strength = 0
        for hand in itertools.combinations(cards, 5):
            hand = poker_types.Cards(cards=hand)
            hand_value = hand.value
            strength = five_card_strength_lookup_table[hand_value]
            if strength > best_strength:
                best_strength = strength
        lookup_table[card_value] = best_strength
    return lookup_table


def write_lookup_table(lookup_table, file_name):
    with open(file_name, 'w') as out:
        for hand, strength in lookup_table.items():
            out.write(f'{hand},{strength}\n')


def read_lookup_table(file_name):
    lookup_table = {}
    with open(file_name, 'r') as infile:
        for line in infile.readlines():
            hand, strength = line.strip().split(',')
            lookup_table[int(hand)] = int(strength)
    return lookup_table


if __name__ == '__main__':
    seven_card_strength_lookup = build_seven_card_strength_lookup_table()
    write_lookup_table(seven_card_strength_lookup, 'seven_card_strength_lookup.csv')
    # seven_card_strength_lookup = build_seven_card_strength_lookup_table()
    pass
