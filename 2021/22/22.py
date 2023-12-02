import re
from itertools import product
from tqdm import tqdm


def load_reboot_steps(file: str) -> list[dict[str, str | tuple[int, int]]]:
    steps = []
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            match = re.search(
                r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)",
                line,
            )
            assert match is not None
            steps.append(
                {
                    "action": match.group(1),
                    "x": (int(match.group(2)), int(match.group(3))),
                    "y": (int(match.group(4)), int(match.group(5))),
                    "z": (int(match.group(6)), int(match.group(7))),
                }
            )

    return steps


def run_reboot(steps: list[dict[str, str | tuple[int, int]]]) -> int:
    on_cubes = set()
    for step in steps:
        action = step["action"]
        x_range: tuple[int, int] = step["x"]
        y_range: tuple[int, int] = step["y"]
        z_range: tuple[int, int] = step["z"]

        # If totally out of range, then fully exclude
        if (
            min(x_range) > 50
            or min(y_range) > 50
            or min(z_range) > 50
            or max(x_range) < -50
            or max(y_range) < -50
            or max(z_range) < -50
        ):
            continue

        # If partially out of range, then adjust the range
        x_range = (max(x_range[0], -50), min(x_range[1], 50))
        y_range = (max(y_range[0], -50), min(y_range[1], 50))
        z_range = (max(z_range[0], -50), min(z_range[1], 50))

        for x in range(x_range[0], x_range[1] + 1):
            for y in range(y_range[0], y_range[1] + 1):
                for z in range(z_range[0], z_range[1] + 1):
                    # if x == 10 and y == -36 and z == 10:
                    #     print(step)

                    if action == "on":
                        on_cubes.add((x, y, z))
                    elif action == "off":
                        if (x, y, z) in on_cubes:
                            on_cubes.remove((x, y, z))

    return len(on_cubes)


def run_reboot_v2(steps: list[dict[str, str | tuple[int, int]]]) -> int:
    x_cuts: list[int] = []
    y_cuts: list[int] = []
    z_cuts: list[int] = []

    # Generate the possible zones
    for step in steps:
        x_cuts.append(step["x"][0])
        x_cuts.append(step["x"][1])
        y_cuts.append(step["y"][0])
        y_cuts.append(step["y"][1])
        z_cuts.append(step["z"][0])
        z_cuts.append(step["z"][1])

    x_cuts = sorted(list(set(x_cuts)))
    y_cuts = sorted(list(set(y_cuts)))
    z_cuts = sorted(list(set(z_cuts)))

    x_ranges = []
    for cut in range(len(x_cuts)):
        x_ranges.append((x_cuts[cut], x_cuts[cut]))
        if cut == len(x_cuts) - 1:
            continue
        if x_cuts[cut + 1] - x_cuts[cut] >= 1:
            x_ranges.append((x_cuts[cut] + 1, x_cuts[cut + 1] - 1))

    y_ranges = []
    for cut in range(len(y_cuts)):
        y_ranges.append((y_cuts[cut], y_cuts[cut]))
        if cut == len(y_cuts) - 1:
            continue
        if y_cuts[cut + 1] - y_cuts[cut] >= 1:
            y_ranges.append((y_cuts[cut] + 1, y_cuts[cut + 1] - 1))

    z_ranges = []
    for cut in range(len(z_cuts)):
        z_ranges.append((z_cuts[cut], z_cuts[cut]))
        if cut == len(z_cuts) - 1:
            continue
        if z_cuts[cut + 1] - z_cuts[cut] >= 1:
            z_ranges.append((z_cuts[cut] + 1, z_cuts[cut + 1] - 1))

    zones = product(x_ranges, y_ranges, z_ranges)
    # print(len(x_cuts), len(y_cuts), len(z_cuts))
    # print(len(x_ranges), len(y_ranges), len(z_ranges))

    # We will want to go through them in reverse order, since we only need the last one
    steps.reverse()
    on_zones = []
    total_on_cubes = 0
    for zone in tqdm(zones, total=len(x_ranges) * len(y_ranges) * len(z_ranges)):
        for index, step in enumerate(steps):
            action = step["action"]

            if not check_if_zone_in_range(zone, step):
                continue

            if action == "on":
                # if zone == ((9, 17), (-36, -34), (7, 12)):
                #     print(step)
                x_range = zone[0]
                y_range = zone[1]
                z_range = zone[2]

                total_on_cubes += (
                    (x_range[1] - x_range[0] + 1)
                    * (y_range[1] - y_range[0] + 1)
                    * (z_range[1] - z_range[0] + 1)
                )

            # print(f"Zone {zone} is {action} by step {index}")
            # print(f"{index},{zone[0][0]},{zone[1][0]},{zone[2][0]},{1 if action == 'on' else 0}")

            break
        else:
            pass
            # print(f"Zone {zone} is off by default")
            # print(f"X,{zone[0][0]},{zone[1][0]},{zone[2][0]},0")

    # Get the number of on cubes

    # all_cubes = set()
    # for on_zone in on_zones:
    #     x_range = on_zone[0]
    #     y_range = on_zone[1]
    #     z_range = on_zone[2]
    #
    #     for x in range(x_range[0], x_range[1] + 1):
    #         for y in range(y_range[0], y_range[1] + 1):
    #             for z in range(z_range[0], z_range[1] + 1):
    #                 all_cubes.add((x, y, z))
    #                 if x == 10 and y == -36 and z == 10:
    #                     print(on_zone)
    #
    # return len(all_cubes), all_cubes
    return total_on_cubes


def check_if_zone_in_range(
    zone: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    step: dict[str, str | tuple[int, int]],
) -> bool:
    zone_x_range = zone[0]
    zone_y_range = zone[1]
    zone_z_range = zone[2]

    if (
        zone_x_range[0] > step["x"][1]
        or zone_x_range[1] < step["x"][0]
        or zone_y_range[0] > step["y"][1]
        or zone_y_range[1] < step["y"][0]
        or zone_z_range[0] > step["z"][1]
        or zone_z_range[1] < step["z"][0]
    ):
        return False

    return True


def run_reboot_v3(steps: list[dict[str, str | tuple[int, int]]]) -> int:
    regions = []
    for step in steps:
        regions_to_add = []
        if step["action"] == "on":
            regions_to_add.append(step)

        for region in regions:
            intersection = find_intersection(step, region)
            if intersection is not None:
                regions_to_add.append(intersection)

        regions += regions_to_add

    total_on_cubes = 0
    for region in regions:
        size = (
            (region["x"][1] - region["x"][0] + 1)
            * (region["y"][1] - region["y"][0] + 1)
            * (region["z"][1] - region["z"][0] + 1)
        )
        if region["action"] == "on":
            total_on_cubes += size
        else:
            total_on_cubes -= size

    return total_on_cubes


def find_intersection(
    region_1: dict[str, str | tuple[int, int]],
    region_2: dict[str, str | tuple[int, int]],
) -> dict[str, str | tuple[int, int]] | None:
    x_1: tuple[int, int] = region_1["x"]
    y_1: tuple[int, int] = region_1["y"]
    z_1: tuple[int, int] = region_1["z"]

    x_2: tuple[int, int] = region_2["x"]
    y_2: tuple[int, int] = region_2["y"]
    z_2: tuple[int, int] = region_2["z"]

    if (
        max(x_1) < min(x_2)
        or max(x_2) < min(x_1)
        or max(y_1) < min(y_2)
        or max(y_2) < min(y_1)
        or max(z_1) < min(z_2)
        or max(z_2) < min(z_1)
    ):
        return None

    direction = "on" if region_2["action"] == "off" else "off"
    x_range = tuple(sorted(list(x_1) + list(x_2))[1:3])
    y_range = tuple(sorted(list(y_1) + list(y_2))[1:3])
    z_range = tuple(sorted(list(z_1) + list(z_2))[1:3])

    return {
        "action": direction,
        "x": x_range,
        "y": y_range,
        "z": z_range,
    }


if __name__ == "__main__":
    test_steps_1 = load_reboot_steps("test_input_1.txt")
    num_cubes_test_1 = run_reboot(test_steps_1)
    print(num_cubes_test_1)
    assert num_cubes_test_1 == 39

    # test_steps_1 = load_reboot_steps("test_input_1.txt")
    # num_cubes_test_1_v2 = run_reboot_v2(test_steps_1)
    # print(num_cubes_test_1_v2)
    # assert num_cubes_test_1_v2 == 39

    test_steps_1 = load_reboot_steps("test_input_1.txt")
    num_cubes_test_1_v3 = run_reboot_v3(test_steps_1)
    print(num_cubes_test_1_v3)
    assert num_cubes_test_1_v3 == 39

    test_steps_2 = load_reboot_steps("test_input_2.txt")
    num_cubes_test_2 = run_reboot(test_steps_2)
    print(num_cubes_test_2)
    assert num_cubes_test_2 == 590784

    test_steps_4 = load_reboot_steps("test_input_4.txt")
    num_cubes_test_4 = run_reboot(test_steps_4)
    print(num_cubes_test_4)
    assert num_cubes_test_4 == 590784

    # test_steps_4 = load_reboot_steps("test_input_4.txt")
    # num_cubes_test_4, cubes_v2 = run_reboot_v2(test_steps_4)
    # print(num_cubes_test_4)
    # assert num_cubes_test_4 == 590784

    test_steps_4 = load_reboot_steps("test_input_4.txt")
    num_cubes_test_4 = run_reboot_v3(test_steps_4)
    print(num_cubes_test_4)
    assert num_cubes_test_4 == 590784

    input_steps = load_reboot_steps("input.txt")
    num_cubes_input = run_reboot(input_steps)
    print(num_cubes_input)

    # test_steps_p1 = load_reboot_steps("test_input_p1.txt")
    # num_cubes_test_p1_v2 = run_reboot_v2(test_steps_p1)
    # print(num_cubes_test_p1_v2)

    test_steps_3 = load_reboot_steps("test_input_3.txt")
    num_cubes_test_3 = run_reboot_v3(test_steps_3)
    print(num_cubes_test_3)
    assert num_cubes_test_3 == 2758514936282235
    # num_cubes_input_v2, _ = run_reboot_v2(input_steps)
    # print(num_cubes_input_v2)

    input_steps = load_reboot_steps("input.txt")
    num_cubes_input = run_reboot_v3(input_steps)
    print(num_cubes_input)
