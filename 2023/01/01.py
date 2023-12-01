INTEGERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
INTEGER_WORDS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def get_line_calibration(line: str) -> int:
    first_int = None
    last_int = None
    for char in line:
        if char in INTEGERS:
            if first_int is None:
                first_int = char
            last_int = char

    return int(first_int) * 10 + int(last_int)


def get_line_calibration_v2(line: str) -> int:
    first_int = None
    last_int = None

    for i in range(len(line)):
        if line[i] in INTEGERS:
            if first_int is None:
                first_int = int(line[i])
            last_int = int(line[i])
        else:
            for index, word in enumerate(INTEGER_WORDS):
                if line[i : i + len(word)] == word:
                    if first_int is None:
                        first_int = index
                    last_int = index

    return first_int * 10 + last_int


def get_total_calibration(file: str, version=1) -> int:
    total_calibration = 0
    with open(file) as f:
        for line in f:
            if version == 1:
                total_calibration += get_line_calibration(line)
            else:
                total_calibration += get_line_calibration_v2(line)

    return total_calibration


if __name__ == "__main__":
    test_result = get_total_calibration("test_input.txt")
    print(f"Test result 1: {test_result}")
    assert test_result == 142

    result = get_total_calibration("input.txt")
    print(f"Result 1: {result}")

    test_result_2 = get_total_calibration("test_input_2.txt", 2)
    print(f"Test result 2: {test_result_2}")
    assert test_result_2 == 281

    result_2 = get_total_calibration("input.txt", 2)
    print(f"Result 2: {result_2}")
