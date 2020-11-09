import random

from short_deck import card

MIN_CARD_BIT = card.Rank.SIX * 4 + card.Suit.DIAMONDS
MAX_CARD_BIT = card.Rank.ACE * 4 + card.Suit.SPADES


def generate_all_card_combinations(number_of_cards, excluded_cards=0):
    # TODO: need to make sure this generates all possible cards
    stack = [(0, 0, MIN_CARD_BIT)]
    while stack:
        bitmask, currently_active_bits, current_bit = stack.pop()
        if excluded_cards & bitmask:
            continue
        elif currently_active_bits == number_of_cards:
            yield bitmask
        elif currently_active_bits > number_of_cards:
            continue
        elif current_bit > MAX_CARD_BIT:
            continue
        else:
            stack.append((bitmask, currently_active_bits, current_bit + 1))
            bitmask |= (1 << current_bit)
            stack.append((bitmask, currently_active_bits + 1, current_bit + 1))


def generate_random_cards(number_of_cards, excluded_cards=0):
    # TODO: need to make sure this generates all possible cards
    cards = 0
    current_number_of_cards = 0
    while current_number_of_cards < number_of_cards:
        card = 1 << random.randint(MIN_CARD_BIT, MAX_CARD_BIT)
        if card & (excluded_cards | cards):
            continue
        cards |= card
        current_number_of_cards += 1
    return cards
