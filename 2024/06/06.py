from pdb import set_trace
from tqdm import tqdm

DIRECTION_MAP = {
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
    (-1, 0): (0, 1)
}

def load_input(filename: str) -> tuple[list[list[str]], tuple[int,int]]:
    result = []
    with open(filename, 'r') as f:
        row = 0
        for line in f.readlines():
            result.append(list(line.strip()))
            if "^" in line:
                col = line.index("^")
                start = (row, col)
            row += 1

    return result, start


def patrol(map_: list[list[str]], start: tuple[int, int]) -> tuple[list[list[str]], bool, list[tuple[tuple[int, int], tuple[int, int]]]]:
    current_position = start
    direction = (0, 1)
    patrolled_positions = []
    while True:
        map_[current_position[0]][current_position[1]] = 'X'
        if (current_position, direction) in patrolled_positions:
            return map_, True, patrolled_positions  # We are somewhere we have been before going in the same direction
        patrolled_positions.append((current_position, direction))
        try:
            if (current_position[0] - direction[1]) < 0 or (current_position[1] + direction[0]) < 0:
                raise IndexError
            item_in_next_position = map_[current_position[0] - direction[1]][current_position[1] + direction[0]]
            if item_in_next_position in ["#", "O"]:
                direction = DIRECTION_MAP[direction]
            else:
                current_position = (current_position[0] - direction[1], current_position[1] + direction[0])
        except IndexError:
            #print_map(map_)
            return map_, False, patrolled_positions  # we have hit the edge


def print_map(map_):
    for row in map_:
        print("".join(row))


def score_map(map_):
    score = 0
    for row in map_:
        for item in row:
            if item == "X":
                score += 1
    return score


def find_all_trap_locations(map_, start, positions_to_test):
    trap_locations = []
    unique_positions_to_test = set()
    for position in positions_to_test:
        unique_positions_to_test.add(position[0])
    unique_positions_to_test.remove(start)
    for position in tqdm(unique_positions_to_test):
        row = position[0]
        col = position[1]
        map_to_try = [row[:] for row in map_]
        map_to_try[row][col] = "O"
        _, trapped, _ = patrol(map_to_try, start)
        if trapped:
            trap_locations.append((row, col))

    return len(trap_locations)


if __name__ == "__main__":
    test_map, test_start = load_input("test_input.txt")
    patrolled_test_map, _, test_patrolled_positions = patrol(test_map, test_start)
    test_score = score_map(patrolled_test_map)
    assert test_score == 41

    map_, start = load_input("input.txt")
    patrolled_map, _, patrolled_positions = patrol(map_, start)
    score = score_map(patrolled_map)
    assert score == 5329
    print(score)

    # test_map_2, test_start_2 = load_input("test_input_2.txt")
    # patrolled_test_map_2, test_trapped_2, _ = patrol(test_map_2, test_start_2)
    # assert test_trapped_2

    test_trap_count = find_all_trap_locations(test_map, test_start, test_patrolled_positions)
    assert test_trap_count == 6

    trap_count = find_all_trap_locations(map_, start, patrolled_positions)
    print(trap_count)

