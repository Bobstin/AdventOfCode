INTEGER_STRINGS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


def is_symbol(char: str) -> bool:
    return char not in INTEGER_STRINGS and char != "."


def get_total_part_numbers(file: str) -> tuple[int, int, list[int]]:
    all_lines = []
    with open(file) as f:
        for line in f.readlines():
            all_lines.append(line.strip())

    total_parts_number = 0
    parts_numbers = []
    potential_gears: dict[tuple[int, int], list[int]] = {}
    for index, line in enumerate(all_lines):
        pos = 0
        number_string = ""
        next_to_symbol = False
        adjacent_gears: list[tuple[int, int]] = []
        while pos < len(line):
            if line[pos] not in INTEGER_STRINGS:
                if next_to_symbol:
                    total_parts_number += int(number_string)
                    parts_numbers.append(int(number_string))
                    for gear in adjacent_gears:
                        if gear not in potential_gears:
                            potential_gears[gear] = []
                        potential_gears[gear].append(int(number_string))
                next_to_symbol = False
                number_string = ""
                adjacent_gears = []

            if line[pos] in INTEGER_STRINGS:
                number_string += line[pos]

                # If not already detected as next to a symbol, check if it is
                if not next_to_symbol:
                    if pos > 0 and is_symbol(line[pos - 1]):
                        next_to_symbol = True
                        if line[pos - 1] == "*":
                            adjacent_gears.append((index, pos - 1))
                    if pos < len(line) - 1 and is_symbol(line[pos + 1]):
                        next_to_symbol = True
                        if line[pos + 1] == "*":
                            adjacent_gears.append((index, pos + 1))
                    if index > 0:
                        if pos > 0 and is_symbol(all_lines[index - 1][pos - 1]):
                            next_to_symbol = True
                            if all_lines[index - 1][pos - 1] == "*":
                                adjacent_gears.append((index - 1, pos - 1))
                        if is_symbol(all_lines[index - 1][pos]):
                            next_to_symbol = True
                            if all_lines[index - 1][pos] == "*":
                                adjacent_gears.append((index - 1, pos))
                        if pos < len(line) - 1 and is_symbol(
                            all_lines[index - 1][pos + 1]
                        ):
                            next_to_symbol = True
                            if all_lines[index - 1][pos + 1] == "*":
                                adjacent_gears.append((index - 1, pos + 1))
                    if index < len(all_lines) - 1:
                        if pos > 0 and is_symbol(all_lines[index + 1][pos - 1]):
                            next_to_symbol = True
                            if all_lines[index + 1][pos - 1] == "*":
                                adjacent_gears.append((index + 1, pos - 1))
                        if is_symbol(all_lines[index + 1][pos]):
                            next_to_symbol = True
                            if all_lines[index + 1][pos] == "*":
                                adjacent_gears.append((index + 1, pos))
                        if pos < len(line) - 1 and is_symbol(
                            all_lines[index + 1][pos + 1]
                        ):
                            next_to_symbol = True
                            if all_lines[index + 1][pos + 1] == "*":
                                adjacent_gears.append((index + 1, pos + 1))

            pos += 1

        if next_to_symbol:
            total_parts_number += int(number_string)
            parts_numbers.append(int(number_string))
            for gear in adjacent_gears:
                if gear not in potential_gears:
                    potential_gears[gear] = []
                potential_gears[gear].append(int(number_string))

    total_gear_ratio = 0
    for gear, gear_numbers in potential_gears.items():
        if len(gear_numbers) == 2:
            total_gear_ratio += gear_numbers[0] * gear_numbers[1]

    return total_parts_number, total_gear_ratio, parts_numbers


if __name__ == "__main__":
    test_total_parts_number, test_total_gear_ratio, _ = get_total_part_numbers(
        "test_input.txt"
    )
    print(test_total_parts_number)
    print(test_total_gear_ratio)
    assert test_total_parts_number == 4361
    assert test_total_gear_ratio == 467835

    (
        total_parts_number_actual,
        total_gear_ratio_actual,
        parts_numbers_actual,
    ) = get_total_part_numbers("input.txt")
    print(total_parts_number_actual)
    print(total_gear_ratio_actual)
