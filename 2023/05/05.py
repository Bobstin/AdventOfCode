def parse_input(
    file: str,
) -> tuple[list[int], list[list[list[int]]], list[list[int]]]:
    with open(file) as f:
        seed_line = f.readline()
        seed_line = seed_line.strip()[len("seeds: ") :]
        seeds = [int(num) for num in seed_line.split(" ")]

        f.readline(2)

        lines = f.readlines()
        maps = []
        current_map = []
        for line in lines:
            line = line.strip()
            if line == "":
                maps.append(current_map)
                current_map = []
            elif ":" in line:
                continue
            else:
                current_map.append([int(num) for num in line.split(" ")])

        maps.append(current_map)

        seed_range_pairs = zip(seeds[::2], seeds[1::2])
        seed_ranges = [[pair[0], pair[0] + pair[1] - 1] for pair in seed_range_pairs]

        return seeds, maps, seed_ranges


def get_location_of_seed(seed: int, maps: list[list[list[int]]]) -> int:
    current_value = seed
    for map_ in maps:
        for entry in map_:
            entry_range = range(entry[1], entry[1] + entry[2])
            if current_value in entry_range:
                current_value = current_value + entry[0] - entry[1]
                break

    return current_value


def get_min_location_of_range(
    seed_ranges: list[list[int]], maps: list[list[list[int]]]
) -> int:
    current_ranges = seed_ranges
    for map_ in maps:
        mapped_ranges = []
        for entry in map_:
            entry_range = [entry[1], entry[1] + entry[2] - 1]
            adjustment = entry[0] - entry[1]
            unmapped_ranges = []
            for current_range in current_ranges:
                matched = []
                # Case 1: current_range is completely before entry_range
                if current_range[1] < entry_range[0]:
                    unmapped_ranges.append(current_range)
                    matched += [1]

                # Case 2: current_range is completely after entry_range
                if current_range[0] > entry_range[1]:
                    unmapped_ranges.append(current_range)
                    matched += [2]

                # Case 3: current_range is completely inside entry_range
                if (
                    current_range[0] >= entry_range[0]
                    and current_range[1] <= entry_range[1]
                ):
                    mapped_ranges.append(
                        [
                            current_range[0] + adjustment,
                            current_range[1] + adjustment,
                        ]
                    )
                    matched += [3]

                # Case 4: current_range is partially before entry_range
                if (
                    current_range[0] < entry_range[0]
                    and current_range[1] >= entry_range[0]
                    and current_range[1] <= entry_range[1]
                ):
                    unmapped_ranges.append([current_range[0], entry_range[0] - 1])
                    mapped_ranges.append(
                        [entry_range[0] + adjustment, current_range[1] + adjustment]
                    )
                    matched += [4]

                # Case 5: current_range is partially after entry_range
                if (
                    current_range[0] >= entry_range[0]
                    and current_range[1] > entry_range[1]
                    and current_range[0] <= entry_range[1]
                ):
                    mapped_ranges.append(
                        [current_range[0] + adjustment, entry_range[1] + adjustment]
                    )
                    unmapped_ranges.append([entry_range[1] + 1, current_range[1]])
                    matched += [5]

                # Case 6: Entry range is completely inside current range
                if (
                    current_range[0] < entry_range[0]
                    and current_range[1] > entry_range[1]
                ):
                    unmapped_ranges.append([current_range[0], entry_range[0] - 1])
                    mapped_ranges.append(
                        [entry_range[0] + adjustment, entry_range[1] + adjustment]
                    )
                    unmapped_ranges.append([entry_range[1] + 1, current_range[1]])
                    matched += [6]

                if len(matched) != 1:
                    raise Exception(
                        "Unhandled case: ", matched, current_range, entry_range
                    )
                # else:
                #     raise Exception("Unhandled case: ", current_range, entry_range)

            current_ranges = unmapped_ranges
        current_ranges = unmapped_ranges + mapped_ranges
        # print(current_ranges)

    # print(current_ranges)
    return min([range_[0] for range_ in current_ranges])


def get_all_locations(seeds: list[int], maps: list[list[list[int]]]) -> list[int]:
    return [get_location_of_seed(seed, maps) for seed in seeds]


if __name__ == "__main__":
    test_seeds, test_maps, test_seed_ranges = parse_input("test_input.txt")
    test_locations = get_all_locations(test_seeds, test_maps)
    print(min(test_locations))
    assert test_locations == [82, 43, 86, 35]
    print(get_min_location_of_range(test_seed_ranges, test_maps))
    assert get_min_location_of_range(test_seed_ranges, test_maps) == 46

    actual_seeds, actual_maps, actual_seed_ranges = parse_input("input.txt")
    actual_locations = get_all_locations(actual_seeds, actual_maps)
    print(min(actual_locations))
    print(get_min_location_of_range(actual_seed_ranges, actual_maps))
