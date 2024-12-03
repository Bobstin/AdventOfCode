import re
import pdb

MUL_PATTERN = r"mul\((\d+),(\d+)\)"
DONT_PATTERN = r"mul\((\d+),(\d+)\)|(do\(\))|(don't\(\))"


def score(file: str) -> int:
    with open(file) as f:
        program = f.read()

    program = program.replace("\n", "")

    result = 0

    matches = re.findall(MUL_PATTERN, program)
    for match in matches:
        result += int(match[0]) * int(match[1])

    return result


def score2(file: str) -> int:
    with open(file) as f:
        program = f.read()

    program = program.replace("\n", "")

    result = 0
    enabled = True

    matches = re.findall(DONT_PATTERN, program)
    for match in matches:
        if match[2] == "do()":
            enabled = True
        elif match[3] == "don't()":
            enabled = False
        else:
            if enabled:
                result += int(match[0]) * int(match[1])

    return result


if __name__ == "__main__":
    assert score("test_input.txt") == 161
    print(score("input.txt"))
    assert score2("test_input_2.txt") == 48
    print(score2("input.txt"))

