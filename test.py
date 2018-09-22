def print_hand_distribution(hand_size=5):
    quantities = {hand.name: 0 for hand in HandRank}
    for cards in combinations(36, 5):
        cards = list(Hand(value=cards<<24).cards)
        for hand, evaluator in evaluators.items():
            if evaluator(cards):
                quantities[hand.name] += 1
                break
    for hand, quantity in quantities.items():
        print(hand, quantity)
