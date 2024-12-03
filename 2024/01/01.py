import pdb

def load_input(file: str) -> list[list[int]]:
    with open(file) as f:
        lines = [line.split(" ") for line in f.readlines()]

    results = [[],[]]
    for line in lines:
        results[0].append(int(line[0]))
        results[1].append(int(line[3].strip()))

    return results


def calculate_distance(data: list[list[int]]) -> int:
    l0 = sorted(data[0])
    l1 = sorted(data[1])
    total_distance = 0
    for index in range(len(l0)):
        # pdb.set_trace()
        total_distance += abs(l0[index] - l1[index])

    return total_distance


def calculate_similarity(data: list[list[int]]) -> int:
    l0 = sorted(data[0])
    l1 = sorted(data[1])
    total_similarity = 0

    l1_freqs = {}
    for value in l1:
        if value not in l1_freqs:
            l1_freqs[value] = 0
        l1_freqs[value] += 1

    for index in range(len(l0)):
        if l0[index] in l1_freqs:
            total_similarity += l0[index] * l1_freqs[l0[index]]

    return total_similarity


if __name__ == "__main__":
    test_input = load_input("test_input.txt")
    test_distance = calculate_distance(test_input)
    test_similarity = calculate_similarity(test_input)
    assert test_distance == 11
    assert test_similarity == 31

    puzzle_input = load_input("input.txt")
    distance = calculate_distance(puzzle_input)
    similarity = calculate_similarity(puzzle_input)
    print(f"Distance: {distance}")
    print(f"Similarity: {similarity}")
