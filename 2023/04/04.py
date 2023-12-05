def parse_cards(file: str) -> list[list[set[int]]]:
    all_cards = []
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()

            # Split the line into the winning and your parts
            split = line.split("|")

            # For the winning part, remove the card number and the colon
            winning_part = split[0]
            winning_part = winning_part[winning_part.find(":") + 2 :].strip()
            winning_numbers = [int(num) for num in winning_part.split(" ") if num != ""]
            winning_numbers_set = set(winning_numbers)
            if len(winning_numbers_set) != len(winning_numbers):
                raise Exception("Duplicate numbers in winning set")

            your_part = split[1].strip()
            your_numbers = [int(num) for num in your_part.split(" ") if num != ""]
            your_numbers_set = set(your_numbers)
            if len(your_numbers_set) != len(your_numbers):
                raise Exception("Duplicate numbers in your set")

            all_cards.append([winning_numbers_set, your_numbers_set])

    return all_cards


def score_cards(cards: list[list[set[int]]]) -> int:
    total_score = 0
    for card in cards:
        winning_numbers, your_numbers = card
        intersection = winning_numbers.intersection(your_numbers)
        if len(intersection) > 0:
            total_score += 2 ** (len(intersection) - 1)

    return total_score


def score_cards_pt2(cards: list[list[set[int]]]) -> int:
    card_count = [1 for _ in range(len(cards))]
    for index, card in enumerate(cards):
        winning_numbers, your_numbers = card
        intersection = winning_numbers.intersection(your_numbers)
        current_card_count = card_count[index]
        for i in range(len(intersection)):
            card_count[index + i + 1] += current_card_count

    return sum(card_count)


if __name__ == "__main__":
    test_cards = parse_cards("test_input.txt")
    test_score = score_cards(test_cards)
    print(test_score)
    assert test_score == 13
    test_score_pt2 = score_cards_pt2(test_cards)
    print(test_score_pt2)
    assert test_score_pt2 == 30

    actual_cards = parse_cards("input.txt")
    actual_score = score_cards(actual_cards)
    print(actual_score)
    actual_score_pt2 = score_cards_pt2(actual_cards)
    print(actual_score_pt2)
