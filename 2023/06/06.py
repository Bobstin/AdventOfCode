from math import sqrt, floor, ceil


def get_product_of_num_possible_wins(races: list[tuple[int, int]]) -> int:
    total = 1
    for race in races:
        determinant = sqrt(race[0] ** 2 - 4 * race[1])
        adjustment = 2 if determinant.is_integer() else 0
        min_wait = ceil((race[0] - determinant) / 2)
        max_wait = floor((race[0] + determinant) / 2)
        total *= max_wait - min_wait + 1 - adjustment

    return total


if __name__ == "__main__":
    test_races = [(7, 9), (15, 40), (30, 200)]
    actual_races = [(54, 239), (70, 1142), (82, 1295), (75, 1253)]

    test_races_2 = [(71530, 940200)]
    actual_races_2 = [(54708275, 239114212951253)]

    test_total = get_product_of_num_possible_wins(test_races)
    print(test_total)
    assert test_total == 288

    test_total_2 = get_product_of_num_possible_wins(test_races_2)
    print(test_total_2)
    assert test_total_2 == 71503

    actual_total = get_product_of_num_possible_wins(actual_races)
    print(actual_total)

    actual_total_2 = get_product_of_num_possible_wins(actual_races_2)
    print(actual_total_2)
