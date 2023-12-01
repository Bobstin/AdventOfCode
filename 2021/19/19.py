from itertools import permutations, product

POSSIBLE_ROTATIONS = list(permutations([0, 1, 2], 3))
POSSIBLE_ORIENTATIONS = list(product([1, -1], [1, -1], [1, -1]))
POSSIBLE_TRANSFORMATIONS = list(product(POSSIBLE_ROTATIONS, POSSIBLE_ORIENTATIONS))


def parse_input(file: str) -> list[list[tuple[int, int, int]]]:
    with open(file) as f:
        scanners: list[list[tuple[int, int, int]]] = []
        current_scanner: list[tuple[int, int, int]] = []
        for line in f.readlines():
            line = line.strip()
            if line == "":
                scanners.append(current_scanner)
                current_scanner = []
            elif line[:3] == "---":
                continue
            else:
                entry = line.split(",")
                current_scanner.append((int(entry[0]), int(entry[1]), int(entry[2])))
        scanners.append(current_scanner)

    return scanners


def transform_scanner(
    scanner: list[tuple[int, int, int]],
    rotation: tuple[int, int, int],
    orientation: tuple[int, int, int],
) -> list[tuple[int, int, int]]:
    result = []
    for ping in scanner:
        new_ping = []
        for i in range(3):
            new_ping.append(ping[rotation[i]] * orientation[i])

        result.append(new_ping)

    return result


def shift_scanner(
    scanner: list[tuple[int, int, int]], shift: list[int]
) -> list[tuple[int, int, int]]:
    result = []
    for ping in scanner:
        new_ping = (ping[0] + shift[0], ping[1] + shift[1], ping[2] + shift[2])
        result.append(new_ping)

    return result


def check_for_transformed_scanner_overlap(
    scanner_1: list[tuple[int, int, int]], scanner_2: list[tuple[int, int, int]]
) -> tuple[list[int], list[tuple[int, int, int]]] | tuple[None, None]:
    for ping_1 in scanner_1:
        for ping_2 in scanner_2:
            delta = [
                ping_1[0] - ping_2[0],
                ping_1[1] - ping_2[1],
                ping_1[2] - ping_2[2],
            ]
            shifted_scanner_2 = shift_scanner(scanner_2, delta)
            if len(set(scanner_1) & set(shifted_scanner_2)) >= 12:
                return delta, shifted_scanner_2

    return None, None


def compare_scanners(
    scanner_1: list[tuple[int, int, int]], scanner_2: list[tuple[int, int, int]]
) -> tuple[list[int], list[tuple[int, int, int]]] | tuple[None, None]:
    for transformation in POSSIBLE_TRANSFORMATIONS:
        transformed_scanner_2 = transform_scanner(scanner_2, *transformation)
        delta, shifted_scanner_2 = check_for_transformed_scanner_overlap(
            scanner_1, transformed_scanner_2
        )
        if delta is not None:
            return delta, shifted_scanner_2

    return None, None


def get_max_manhattan_distance(deltas: list[list[int]]) -> int:
    distances = []
    for delta_combination in product(deltas, deltas):
        distance = (
            abs(delta_combination[0][0] - delta_combination[1][0])
            + abs(delta_combination[0][1] - delta_combination[1][1])
            + abs(delta_combination[0][2] - delta_combination[1][2])
        )
        distances.append(distance)

    return max(distances)


def find_unique_beacons(scanners: list[list[tuple[int, int, int]]]) -> tuple[int, int]:
    scanners_in_primary_coordinate_system = [scanners[0]]
    unmatched_scanners = scanners[1:]
    scanner_deltas = [[0, 0, 0]]

    while len(unmatched_scanners) > 0:
        new_scanners_in_primary_coordinate_system = (
            scanners_in_primary_coordinate_system.copy()
        )
        new_unmatched_scanners = []
        new_scanner_deltas = scanner_deltas.copy()
        for i, unmatched_scanner in enumerate(unmatched_scanners):
            for j, scanner_in_primary_coordinate_system in enumerate(
                scanners_in_primary_coordinate_system
            ):
                delta, transformed_scanner = compare_scanners(
                    scanner_in_primary_coordinate_system, unmatched_scanner
                )
                if transformed_scanner is not None:
                    new_scanners_in_primary_coordinate_system.append(
                        transformed_scanner
                    )
                    new_scanner_deltas.append(delta)
                    break
            else:
                new_unmatched_scanners.append(unmatched_scanner)

        unmatched_scanners = new_unmatched_scanners.copy()
        scanners_in_primary_coordinate_system = (
            new_scanners_in_primary_coordinate_system.copy()
        )
        scanner_deltas = new_scanner_deltas.copy()
        print(
            len(scanners_in_primary_coordinate_system)
            / (len(scanners_in_primary_coordinate_system) + len(unmatched_scanners))
        )

    unique_beacons: set[tuple[int, int, int]] = set()
    for scanner in scanners_in_primary_coordinate_system:
        unique_beacons = unique_beacons | set(scanner)

    max_manhattan_distance = get_max_manhattan_distance(scanner_deltas)

    return len(unique_beacons), max_manhattan_distance


if __name__ == "__main__":
    test_scanners = parse_input("test_input.txt")
    test_unique_beacons = find_unique_beacons(test_scanners)
    assert test_unique_beacons == (79, 3621)
    print(test_unique_beacons)
    print("---\n")

    scanners = parse_input("input.txt")
    print(find_unique_beacons(scanners))
