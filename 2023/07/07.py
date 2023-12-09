class Hand:
    def __init__(self, hand_str):
        self.cards = [card_str for card_str in hand_str.split(" ")[0]]
        self.bid = int(hand_str.split(" ")[1])

    def __repr__(self):
        return f"{''.join(self.cards)} {self.bid}"

    def get_hand_counts(self, cards) -> dict[str, int]:
        counts = {}
        for card in cards:
            if card in counts:
                counts[card] += 1
            else:
                counts[card] = 1

        return counts

    def get_hand_type(self, cards):
        counts = self.get_hand_counts(cards)

        if max(counts.values()) == 5:
            return 7
        elif max(counts.values()) == 4:
            return 6
        elif 3 in counts.values() and 2 in counts.values():
            return 5
        elif max(counts.values()) == 3:
            return 4
        elif list(counts.values()).count(2) == 2:
            return 3
        elif 2 in counts.values():
            return 2
        else:
            return 1

    card_scores = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def __lt__(self, other):
        self_type = self.get_hand_type(self.cards)
        other_type = self.get_hand_type(other.cards)
        if self_type != other_type:
            return self_type < other_type

        for index, card in enumerate(self.cards):
            if card != other.cards[index]:
                return self.card_scores[card] < self.card_scores[other.cards[index]]


class HandPt2(Hand):
    def get_hand_counts(self, cards) -> dict[str, int]:
        if cards == ["J", "J", "J", "J", "J"]:
            return {"J": 5}

        counts: dict[str, int] = {}
        num_jokers = cards.count("J")
        for card in cards:
            if card == "J":
                continue

            if card in counts:
                counts[card] += 1
            else:
                counts[card] = 1

        most_common_card = max(counts.items(), key=lambda l: l[1])[0]
        counts[most_common_card] += num_jokers

        return counts

    card_scores = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 0,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }


def parse_input(file: str, hand_type=1) -> list[Hand]:
    with open(file) as f:
        lines = f.readlines()

        if hand_type == 1:
            hands = [Hand(line.strip()) for line in lines]
        else:
            hands = [HandPt2(line.strip()) for line in lines]

        return hands


def get_total_winnings(hands: list[Hand]) -> int:
    hands = sorted(hands)
    total_winnings = 0
    for index, hand in enumerate(hands):
        total_winnings += hand.bid * (index + 1)

    return total_winnings


if __name__ == "__main__":
    test_hands = parse_input("test_input.txt")
    test_total_winnings = get_total_winnings(test_hands)
    print(test_total_winnings)
    assert test_total_winnings == 6440

    test_hands_2 = parse_input("test_input.txt", 2)
    test_total_winnings_2 = get_total_winnings(test_hands_2)
    print(test_total_winnings_2)
    assert test_total_winnings_2 == 5905

    actual_hands = parse_input("input.txt")
    actual_total_winnings = get_total_winnings(actual_hands)
    print(actual_total_winnings)

    actual_hands_2 = parse_input("input.txt", 2)
    actual_total_winnings_2 = get_total_winnings(actual_hands_2)
    print(actual_total_winnings_2)
