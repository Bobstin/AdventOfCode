import re

MAX_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def load_games(file: str) -> dict[int, list[list[tuple[int, str]]]]:
    games = {}
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            game_id = int(re.search(r"Game (\d+):", line).group(1))
            pull_sets = re.findall(r"[:;]((?: \d+ (?:red|blue|green),?)+)", line)
            cleaned_pull_sets = []
            for pull_set in pull_sets:
                pulls = re.findall(r"(?:(\d+) (red|blue|green))", pull_set)
                cleaned_pull_sets.append([(int(num), color) for num, color in pulls])
            games[game_id] = cleaned_pull_sets

    return games


def validate_games(games: dict[int, list[list[tuple[int, str]]]]) -> tuple[int, int]:
    valid_games = []
    game_powers = []

    for game_id, pull_sets in games.items():
        valid = True
        min_cubes = {"red": 0, "green": 0, "blue": 0}
        for pull_set in pull_sets:
            for num, color in pull_set:
                if num > MAX_CUBES[color]:
                    valid = False
                min_cubes[color] = max(min_cubes[color], num)

        if valid:
            valid_games.append(game_id)

        game_powers.append(min_cubes["red"] * min_cubes["green"] * min_cubes["blue"])

    return sum(valid_games), sum(game_powers)


if __name__ == "__main__":
    test_games = load_games("test_input.txt")
    test_valid_id_sum = validate_games(test_games)
    print(test_valid_id_sum)
    assert test_valid_id_sum == (8, 2286)

    input_games = load_games("input.txt")
    valid_id_sum = validate_games(input_games)
    print(valid_id_sum)
