from math import floor

NEXT_TILE = {
    "|": {(0, -1): (0, -1), (0, 1): (0, 1)},
    "-": {(1, 0): (1, 0), (-1, 0): (-1, 0)},
    "L": {(0, 1): (1, 0), (-1, 0): (0, -1)},
    "J": {(1, 0): (0, -1), (0, 1): (-1, 0)},
    "7": {(1, 0): (0, 1), (0, -1): (-1, 0)},
    "F": {(0, -1): (1, 0), (-1, 0): (0, 1)},
}

POSSIBLE_DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def parse(file: str) -> tuple[tuple[int, int], dict[tuple[int, int], str], int, int]:
    result = {}
    start = None
    with open(file) as f:
        y = 0
        for line in f.readlines():
            line = line.strip()
            for index, char in enumerate(line):
                result[(index, y)] = char
                if char == "S":
                    start = (index, y)
            y += 1

    if start is None:
        raise ValueError("No start found")

    return start, result, len(line) - 1, y - 1


def traverse_pipe(
    start: tuple[int, int], map_: dict[tuple[int, int], str]
) -> tuple[int, set[tuple[int, int]]]:
    position = start

    for direction in POSSIBLE_DIRECTIONS:
        # Check if that pipe points to the start
        test_next_position = (position[0] + direction[0], position[1] + direction[1])
        test_next_pipe_type = map_[test_next_position]
        if test_next_pipe_type == ".":
            continue
        if (-1 * direction[0], -1 * direction[1]) not in NEXT_TILE[
            test_next_pipe_type
        ].values():
            continue

        # Otherwise, traverse the pipe
        num_steps = 0
        pipe_locations = set()
        while True:
            num_steps += 1
            pipe_locations.add(position)
            position = (position[0] + direction[0], position[1] + direction[1])
            pipe_type = map_[position]
            if pipe_type == "S":
                return floor(num_steps / 2), pipe_locations
            else:
                direction = NEXT_TILE[pipe_type][direction]


def find_inside_pipe_locations(
    start: tuple[int, int],
    map_: dict[tuple[int, int], str],
    start_override: str,
    max_x: int,
    max_y: int,
    pipe_locations: set[tuple[int, int]],
) -> int:
    # We need the actual type of the start. This could be detected, but it was a lot easier to just visually look at it
    map_[start] = start_override

    # We need to keep track of what has been detected as being outside
    # As well as what border positions have not been checked
    positions_to_check = set()

    # Get all of the border positions.
    for i in range(max_x + 1):
        positions_to_check.add((i, 0))
        positions_to_check.add((i, max_y))
    for i in range(1, max_y):
        positions_to_check.add((0, i))
        positions_to_check.add((max_x, i))

    # Remove the border positions which are included in the pipe. These are all outside
    positions_to_check = positions_to_check - pipe_locations
    outside_pipe_locations = positions_to_check.copy()

    # Start with a position on the border, then fill - these are all not in the loop
    while len(positions_to_check) > 0:
        position = positions_to_check.pop()
        for direction in POSSIBLE_DIRECTIONS:
            adjacent_position = (
                position[0] + direction[0],
                position[1] + direction[1],
            )
            # Check if we have already checked this position
            if adjacent_position in outside_pipe_locations:
                continue

            # Check if this position is outside the map
            if (
                adjacent_position[0] > max_x
                or adjacent_position[1] > max_y
                or adjacent_position[0] < 0
                or adjacent_position[1] < 0
            ):
                continue

            # If it is in the pipe, we need to see if it is blocked
            # This depends on direction; verticals are blocked by -, and horizontals are blocked by |
            # If not blocked, then we need to adjust the adjacent
            blocking_char = "|" if direction[0] != 0 else "-"
            while adjacent_position in pipe_locations:
                if map_[adjacent_position] == blocking_char:
                    break
                if (
                    adjacent_position[0] > max_x
                    or adjacent_position[1] > max_y
                    or adjacent_position[0] < 0
                    or adjacent_position[1] < 0
                ):
                    break
                else:
                    adjacent_position = (
                        adjacent_position[0] + direction[0],
                        adjacent_position[1] + direction[1],
                    )

            # If we didn't break (i.e. we were not blocked) then this position is outside, and needs to be added to the to be checked set
            else:
                outside_map = (
                    adjacent_position[0] > max_x
                    or adjacent_position[1] > max_y
                    or adjacent_position[0] < 0
                    or adjacent_position[1] < 0
                )
                if adjacent_position not in outside_pipe_locations and not outside_map:
                    if adjacent_position == (7, 4):
                        print(adjacent_position)
                    outside_pipe_locations.add(adjacent_position)
                    positions_to_check.add(adjacent_position)
                    continue

    return (
        ((max_x + 1) * ((max_y + 1) * 1))
        - len(outside_pipe_locations)
        - len(pipe_locations)
    )


if __name__ == "__main__":
    test_1_start, test_1_map, max_x_1, max_y_1 = parse("test_input_1.txt")
    test_distance_1, pipe_locations_1 = traverse_pipe(test_1_start, test_1_map)
    # print(test_distance_1)
    assert test_distance_1 == 4
    # inside_pipe_count_1 = find_inside_pipe_locations(
    #     test_1_start, test_1_map, "F", max_x_1, max_y_1, pipe_locations_1
    # )
    # # print(inside_pipe_count_1)
    # assert inside_pipe_count_1 == 1

    test_2_start, test_2_map, max_x_2, max_y_2 = parse("test_input_2.txt")
    test_distance_2, pipe_locations_2 = traverse_pipe(test_2_start, test_2_map)
    # print(test_distance_2)
    assert test_distance_2 == 8

    test_3_start, test_3_map, max_x_3, max_y_3 = parse("test_input_3.txt")
    test_distance_3, pipe_locations_3 = traverse_pipe(test_3_start, test_3_map)
    # print(test_distance_1)
    # inside_pipe_count_3 = find_inside_pipe_locations(
    #     test_3_start, test_3_map, "F", max_x_3, max_y_3, pipe_locations_3
    # )
    # assert inside_pipe_count_3 == 4

    test_4_start, test_4_map, max_x_4, max_y_4 = parse("test_input_4.txt")
    test_distance_4, pipe_locations_4 = traverse_pipe(test_4_start, test_4_map)
    # inside_pipe_count_4 = find_inside_pipe_locations(
    #     test_4_start, test_4_map, "F", max_x_4, max_y_4, pipe_locations_4
    # )
    # assert inside_pipe_count_4 == 4

    test_5_start, test_5_map, max_x_5, max_y_5 = parse("test_input_5.txt")
    test_distance_5, pipe_locations_5 = traverse_pipe(test_5_start, test_5_map)
    inside_pipe_count_5 = find_inside_pipe_locations(
        test_5_start, test_5_map, "F", max_x_5, max_y_5, pipe_locations_5
    )
    print(inside_pipe_count_5)
    assert inside_pipe_count_5 == 8

    puzzle_start, puzzle_map, puzzle_max_x, puzzle_max_y = parse("input.txt")
    puzzle_distance, puzzle_pipe_locations = traverse_pipe(puzzle_start, puzzle_map)
    # print(puzzle_distance)
