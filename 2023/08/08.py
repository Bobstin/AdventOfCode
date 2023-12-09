import re
from math import lcm


def parse_map(file: str) -> dict[str : dict[str, str]]:
    with open(file) as f:
        lines = f.readlines()

        result = {}
        for line in lines:
            line = line.strip()
            match = re.search(r"(\D{3}) = \((\D{3}), (\D{3})\)", line)
            assert match is not None
            result[match.group(1)] = {"L": match.group(2), "R": match.group(3)}

        return result


def follow_map(
    map_: dict[str, dict[str, str]], path: str, start="AAA", end: str | None = "ZZZ"
) -> int:
    position = start
    num_steps = 0

    # pbar = tqdm()
    while True:
        for step in path:
            # pbar.update(1)
            num_steps += 1
            position = map_[position][step]
            if end is None and position[2] == "Z":
                return num_steps

            elif position == end:
                return num_steps

            # This was a check to see if I missed any other ends in the loop
            elif position[2] == "Z":
                print(position, num_steps)


def get_node_combinations(
    map_: dict[str, dict[str, str]]
) -> tuple[list[str], list[str]]:
    possible_starts = []
    possible_ends = []
    for node in map_.keys():
        if node[2] == "Z":
            possible_ends.append(node)
        elif node[2] == "A":
            possible_starts.append(node)

    return possible_starts, possible_ends


def follow_ghost_map(map_: dict[str, dict[str, str]], path: str) -> int:
    possible_starts, _ = get_node_combinations(map_)
    loop_lengths = [follow_map(map_, path, start, None) for start in possible_starts]
    return lcm(*loop_lengths)


if __name__ == "__main__":
    test_map = parse_map("test_input_1.txt")
    test_steps_1 = follow_map(test_map, "RL")
    assert test_steps_1 == 2

    test_map_2 = parse_map("test_input_2.txt")
    test_steps_2 = follow_map(test_map_2, "LLR")
    assert test_steps_2 == 6

    actual_map = parse_map("input.txt")
    actual_path = "LLRRRLLRLRRRLLRLRLRLRLRRRLRRLRRLRLLLRRLLRRLRRLRRLRRRLLLRRLRLRRRLRRRLRLRRLRRRLRLRRRLRLRLLLRLRRLRLRRLRRRLRLRRRLRRRLRRRLRRRLRLRRRLRRRLRLLRRLRLRLRRRLRRLRRRLRRRLRRRLRRRLLLLRRLLRLRRLRRLRRRLRRRLLLRRLRRLRLRRLRRRLRRLRLRRRLRLRRLLRLLRRLRLRRRLRRLRRLRLRRLLLRRRLRLRRRLRLRLLRLRLRRRLRLRLRRRLRRLRRLRRRLRRLLRRRR"
    actual_steps = follow_map(actual_map, actual_path)
    print(actual_steps)

    actual_ghost_steps = follow_ghost_map(actual_map, actual_path)
    print(actual_ghost_steps)

    # I did some additional testing, because this method assumes three things:
    # 1. From any given start, you only ever touch one end
    # 2. The path from a start to and end is a full multiple of the path length
    # 3. The path from an end to itself is equal to the path from the start to its end
    actual_steps_test_1 = follow_map(actual_map, actual_path, "ZZZ", "ZZZ")
    actual_steps_test_2 = follow_map(actual_map, actual_path, "GPA", "CVZ")
    actual_steps_test_3 = follow_map(actual_map, actual_path, "CVZ", "CVZ")
    actual_steps_test_4 = follow_map(actual_map, actual_path, "GTA", "FPZ")
    actual_steps_test_5 = follow_map(actual_map, actual_path, "FPZ", "FPZ")
    actual_steps_test_6 = follow_map(actual_map, actual_path, "VDA", "STZ")
    actual_steps_test_7 = follow_map(actual_map, actual_path, "STZ", "STZ")
    actual_steps_test_8 = follow_map(actual_map, actual_path, "AAA", "ZZZ")
    actual_steps_test_9 = follow_map(actual_map, actual_path, "ZZZ", "ZZZ")
    actual_steps_test_A = follow_map(actual_map, actual_path, "VSA", "MKZ")
    actual_steps_test_B = follow_map(actual_map, actual_path, "MKZ", "MKZ")
    actual_steps_test_C = follow_map(actual_map, actual_path, "BBA", "SKZ")
    actual_steps_test_D = follow_map(actual_map, actual_path, "SKZ", "SKZ")

    assert actual_steps_test_2 % len(actual_path) == 0
    assert actual_steps_test_4 % len(actual_path) == 0
    assert actual_steps_test_6 % len(actual_path) == 0
    assert actual_steps_test_8 % len(actual_path) == 0
    assert actual_steps_test_A % len(actual_path) == 0
    assert actual_steps_test_C % len(actual_path) == 0

    assert actual_steps_test_2 == actual_steps_test_3
    assert actual_steps_test_4 == actual_steps_test_5
    assert actual_steps_test_6 == actual_steps_test_7
    assert actual_steps_test_8 == actual_steps_test_9
    assert actual_steps_test_A == actual_steps_test_B
    assert actual_steps_test_C == actual_steps_test_D
