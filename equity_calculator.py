import functools
import operator
import random

import range_expander
import hand_evaluator
import card_generators


def _build_hands(hand_ranges, players):
    # items of hand_ranges are a tuple in the form (player_number, hand)
    random.shuffle(hand_ranges)
    for hand_choice in hand_ranges:
        chosen_player, chosen_hand = hand_choice
        # remove all hands that are from the same player as chosen hand
        possible_hands = [(player, hand) for player, hand in hand_ranges
                          if player != chosen_player]
        # remove all hands that share a card with the chosen hand
        possible_hands = [(player, hand) for player, hand in possible_hands
                          if not (hand & chosen_hand)]
        # check that there are still valid choices for all the other players
        remaining_players = {player for player in players if player != chosen_player}
        players_in_possible_hands = {player for player, hand in possible_hands}
        if remaining_players != players_in_possible_hands:
            continue
        if not remaining_players:
            return [hand_choice]
        other_hands = _build_hands(possible_hands, remaining_players)
        if other_hands:
            return [hand_choice] + other_hands


def choose_hands_from_hand_ranges(hand_ranges, board=0):
    """Picks a random hand from each players hand range, making sure none of the chosen hands share the same card."""
    # choosing player1's hand first every time may lead to a non uniform selection of other players hands
    # if one players hands all contain the same card, hands with that card must be removed from the other players hand ranges
    players = list(range(len(hand_ranges)))
    hand_ranges = [(i, hand) for i, hand_range in enumerate(hand_ranges) for hand in hand_range if not (hand & board)]
    player_hands = _build_hands(hand_ranges, players)
    player_hands = sorted(player_hands, key=lambda x: x[0])
    return [hand for player, hand in player_hands]


def compare_hand_ranges(seven_card_strength_lookup, *hand_ranges, board=0, board_size=0, iterations=10000):
    number_of_players = len(hand_ranges)
    player_results = [{'wins': 0, 'ties': 0, 'losses': 0} for _ in range(number_of_players)]
    for _ in range(iterations):
        # TODO: need to make sure chosen hands do not share any cards
        # hands = [random.choice(hand_range) for hand_range in hand_ranges]
        hands = choose_hands_from_hand_ranges(hand_ranges, board)
        taken_cards = board | functools.reduce(operator.or_, hands)
        full_board = board | card_generators.generate_random_cards(5 - board_size, taken_cards)
        hand_strengths = [seven_card_strength_lookup[hands[i] | full_board]
                          for i in range(number_of_players)]
        best_hand = max(hand_strengths)
        best_hands = [i for i in range(number_of_players) if hand_strengths[i] == best_hand]
        for i in range(number_of_players):
            if i in best_hands:
                if len(best_hands) > 1:
                    player_results[i]['ties'] += 1
                else:
                    player_results[i]['wins'] += 1
            else:
                player_results[i]['losses'] += 1
    return player_results


def compare_hand_ranges_exhaustive():
    pass


def main():
    hand_ranges = [[76561193665298432], [720575940379279360, 432345564227567616, 216172782113783808, 360287970189639680, 648518346341351424, 864691128455135232]]
    # print(choose_hands_from_hand_ranges(hand_ranges))

    # if 'seven_card_strength_lookup' not in dir():
    #     seven_card_strength_lookup =  hand_evaluator.read_lookup_table('seven_card_strength_lookup.csv')
    # i = 1
    # hand_ranges = []
    # while True:
    #     print(f'player {i} hand range: ', end='')
    #     hand_range = input()
    #     if not hand_range:
    #         break
    #     hand_ranges.append([hand.value for hand in range_expander.expand_range(hand_range)])
    #     i += 1

    results = compare_hand_ranges(seven_card_strength_lookup, *hand_ranges)
    for result in results:
        print(result)


if __name__ == '__main__':
    main()
