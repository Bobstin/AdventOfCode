def get_next_and_prior_value(initial_history: list[int]) -> tuple[int, int]:
    full_history = [initial_history]
    current_history = initial_history.copy()
    while True:
        new_history = []
        for i in range(len(current_history) - 1):
            new_history.append(current_history[i + 1] - current_history[i])
        full_history.append(new_history)
        current_history = new_history.copy()
        if new_history.count(0) == len(new_history):
            break

    total_last_value = 0
    new_first_value = 0
    full_history = reversed(full_history)
    for history in full_history:
        total_last_value += history[-1]
        new_first_value = history[0] - new_first_value

    return total_last_value, new_first_value


def parse_inputs(file: str) -> list[list[int]]:
    with open(file) as f:
        lines = f.readlines()
        return [[int(num) for num in line.strip().split(" ")] for line in lines]


def get_total_next_and_prior_values(histories: list[list[int]]) -> tuple[int, int]:
    next_and_prior_values = [get_next_and_prior_value(history) for history in histories]
    return sum([value[0] for value in next_and_prior_values]), sum(
        [value[1] for value in next_and_prior_values]
    )


if __name__ == "__main__":
    assert get_next_and_prior_value([0, 3, 6, 9, 12, 15])[0] == 18
    assert get_next_and_prior_value([1, 3, 6, 10, 15, 21])[0] == 28
    assert get_next_and_prior_value([10, 13, 16, 21, 30, 45]) == (68, 5)

    actual_histories = parse_inputs("input.txt")
    print(get_total_next_and_prior_values(actual_histories))
