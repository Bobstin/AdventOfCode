possible_quantum_outcomes = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


def play_game(position_1: int, position_2: int) -> int:
    die = 0  # So that we roll a 1 on the first turn
    num_rolls = 0
    score_1 = 0
    score_2 = 0

    while True:
        # Player 1 goes
        for i in range(3):
            die = (die % 100) + 1
            position_1 += die
            num_rolls += 1
        position_1 = ((position_1 - 1) % 10) + 1
        score_1 += position_1

        if score_1 >= 1000:
            return num_rolls * score_2

        # Player 2 goes
        for i in range(3):
            die = (die % 100) + 1
            position_2 += die
            num_rolls += 1
        position_2 = ((position_2 - 1) % 10) + 1
        score_2 += position_2

        if score_2 >= 1000:
            return score_1 * num_rolls


def play_quantum_game(
    position_1: int,
    position_2: int,
    score_1: int,
    score_2: int,
    die_result: int,
    next_player: int,
) -> list[int]:
    if next_player == 1:
        position_1 = ((position_1 + die_result - 1) % 10) + 1
        subsequent_player = 2
        score_1 += position_1
        if score_1 >= 21:
            return [1, 0]
    else:
        position_2 = ((position_2 + die_result - 1) % 10) + 1
        subsequent_player = 1
        score_2 += position_2
        if score_2 >= 21:
            return [0, 1]

    total_result = [0, 0]
    for i in range(3, 10):
        next_game = play_quantum_game(
            position_1,
            position_2,
            score_1,
            score_2,
            i,
            subsequent_player,
        )
        probability = possible_quantum_outcomes[i]
        total_result[0] += probability * next_game[0]
        total_result[1] += probability * next_game[1]

    return total_result


def quantum_game(position_1: int, position_2: int) -> int:
    global max_total_result
    total_result = [0, 0]
    for i in range(3, 10):
        next_game = play_quantum_game(position_1, position_2, 0, 0, i, 1)
        probability = possible_quantum_outcomes[i]
        total_result[0] += probability * next_game[0]
        total_result[1] += probability * next_game[1]
        print([i, total_result])

    return max(total_result)


if __name__ == "__main__":
    test_result = play_game(4, 8)
    print(test_result)
    assert test_result == 739785

    result = play_game(2, 10)
    print(result)

    test_quantum_result = quantum_game(4, 8)
    print("------")
    print(test_quantum_result)
    assert test_quantum_result == 444356092776315

    quantum_result = quantum_game(2, 10)
    print("------")
    print(quantum_result)
