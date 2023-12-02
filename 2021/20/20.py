def load_inputs(prefix: str) -> tuple[list[int], list[list[int]], int]:
    with open(f"{prefix}algo.txt") as f:
        algo_str = f.read().strip()
        algo = [1 if char == "#" else 0 for char in algo_str]

    with open(f"{prefix}input.txt") as f:
        image = []
        for line in f:
            line = line.strip()
            image.append([1 if char == "#" else 0 for char in line])

    return algo, image, 0


def add_border(image: list[list[int]], void_value) -> list[list[int]]:
    for row in image:
        row.insert(0, void_value)
        row.append(void_value)

    image.insert(0, [void_value for _ in range(len(image[0]))])
    image.append([void_value for _ in range(len(image[0]))])

    return image


def remove_border(image: list[list[int]]) -> list[list[int]]:
    for row in image:
        row.pop(0)
        row.pop()

    image.pop(0)
    image.pop()

    return image


def get_new_pixel(image: list[list[int]], row: int, col: int, algo: list[int]) -> int:
    surrounding_pixels = [
        image[row - 1][col - 1],
        image[row - 1][col],
        image[row - 1][col + 1],
        image[row][col - 1],
        image[row][col],
        image[row][col + 1],
        image[row + 1][col - 1],
        image[row + 1][col],
        image[row + 1][col + 1],
    ]
    combined_pixels = "".join([str(pixel) for pixel in surrounding_pixels])
    return algo[int(combined_pixels, 2)]


def enhance_image(
    algo: list[int], image: list[list[int]], void_value: int
) -> tuple[list[list[int]], int]:
    image = add_border(add_border(image, void_value), void_value)
    new_image = [row.copy() for row in image]
    if void_value == 0:
        new_void_value = algo[0]
    else:
        new_void_value = algo[511]

    for row in range(1, len(image) - 1):
        for col in range(1, len(image[0]) - 1):
            new_image[row][col] = get_new_pixel(image, row, col, algo)

    new_image = remove_border(new_image)

    return new_image, new_void_value


def count_light_pixels(image: list[list[int]]) -> int:
    return sum([sum(row) for row in image])


def multiple_enhancements(
    algo: list[int], image: list[list[int]], void_value: int, num_enhancements: int
) -> tuple[list[list[int]], int]:
    for _ in range(num_enhancements):
        image, void_value = enhance_image(algo, image, void_value)

    return image, void_value


if __name__ == "__main__":
    test_algo, test_image, test_void_value = load_inputs("test_")
    test_image, _ = multiple_enhancements(test_algo, test_image, test_void_value, 2)
    test_light_pixels = count_light_pixels(test_image)
    print(test_light_pixels)
    assert test_light_pixels == 35

    algo, start_image, start_void_value = load_inputs("")
    result_image, _ = multiple_enhancements(algo, start_image, start_void_value, 2)
    light_pixels = count_light_pixels(result_image)
    print(light_pixels)

    result_image, _ = multiple_enhancements(algo, start_image, start_void_value, 50)
    light_pixels = count_light_pixels(result_image)
    print(light_pixels)
