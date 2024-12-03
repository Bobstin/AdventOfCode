import pdb


def parse_input(file: str) -> list[list[int]]:
    result = []
    with open(file) as f:
        for line in f.readlines():
            result.append([int(val) for val in line.split(" ")])

    return result


def check_safe(data: list[int]) -> bool:
    increased = False
    decreased = False
    for i in range(1, len(data)):
        delta = data[i] - data[i - 1]
        if delta == 0:
            return False
        if abs(delta) > 3:
            # print(f"Delta: {delta}")
            return False
        if delta > 0:
            increased = True
            if decreased:
                # print("Decreased then increased")
                return False
        if delta < 0:
            decreased = True
            if increased:
                # print("Increased then decreased")
                return False
    # print(data)
    return True


def check_safe_removed(data: list[int]) -> bool:
    full_safe = check_safe(data)
    if full_safe:
        return True

    for i in range(len(data)):
        #print(i)
        new_data = data[:i] + data[i + 1:]
        if check_safe(new_data):
            return True

    return False


def count_safe(data: list[list[int]], allow_removed: bool) -> int:
    safe_func = check_safe if not allow_removed else check_safe_removed
    count = 0
    for line in data:
        if safe_func(line):
            count += 1

    return count

if __name__ == "__main__":
    test_input = parse_input("test_input.txt")
    assert count_safe(test_input, False) == 2
    assert count_safe(test_input, True) == 4
    puzzle_input = parse_input("input.txt")
    print(count_safe(puzzle_input, False))
    print(count_safe(puzzle_input, True))
