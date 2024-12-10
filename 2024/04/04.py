import pdb


def word_search(file: str) -> int:
    with open(file) as f:
        lines = f.readlines()

    total_matches = 0
    for row, line in enumerate(lines):
        for column, char in enumerate(line):
            if char != "X":
                continue

            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if x == 0 and y == 0:
                        continue

                    word = get_word(lines, row, column, x, y)
                    if word == "XMAS":
                        #print(row, column, x, y)
                        total_matches += 1

    return total_matches


def x_mas_search(file: str) -> int:
    with open(file) as f:
        lines = f.readlines()

    total_matches = 0
    for row, line in enumerate(lines):
        if row == 0:
            continue
        for column, char in enumerate(line):
            if column == 0:
                continue
            if char != "A":
                continue

            try:
                part_1 = lines[row - 1][column - 1] + lines[row + 1][column + 1]
                part_2 = lines[row - 1][column + 1] + lines[row + 1][column - 1]
                if part_1 in ["MS", "SM"] and part_2 in ["MS", "SM"]:
                    total_matches += 1
            except IndexError:
                continue

    return total_matches


def get_word(lines, row, col, x, y) -> str | None:
    if row + 3*x < 0 or col + 3*y < 0:
        return None
    try:
        p1 = lines[row][col]
        p2 = lines[row + x][col + y]
        p3 = lines[row + 2*x][col + 2*y]
        p4 = lines[row + 3*x][col + 3*y]
    except IndexError:
        return None

    return p1 + p2 + p3 + p4


if __name__  == "__main__":
    assert word_search("test_input.txt") == 18
    print(word_search("input.txt"))
    assert x_mas_search("test_input.txt") == 9
    print(x_mas_search("input.txt"))
