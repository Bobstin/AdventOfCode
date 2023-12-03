import re
from tqdm import tqdm


def parse_program(file: str) -> list[dict[str, str | int | None]]:
    commands = []
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            match = re.search(r"(\S*) ([wxyz]) ?(.*)", line)
            assert match is not None
            if match.group(3) == "":
                var_2 = None
            else:
                if match.group(3) in ["w", "x", "y", "z"]:
                    var_2 = match.group(3)
                else:
                    var_2 = int(match.group(3))
            commands.append(
                {
                    "command": match.group(1),
                    "var_1": match.group(2),
                    "var_2": var_2,
                }
            )

    return commands


def run_program(
    program: list[dict[str, str | int | None]], program_input: list[int]
) -> dict[str, int]:
    state = {"w": 0, "x": 0, "y": 0, "z": 0}
    for command in program:
        assert isinstance(command["var_1"], str)

        match command["command"]:
            case "inp":
                next_input = program_input.pop(0)
                state[command["var_1"]] = next_input
            case "add":
                if isinstance(command["var_2"], int):
                    state[command["var_1"]] += command["var_2"]
                else:
                    state[command["var_1"]] += state[command["var_2"]]
            case "mul":
                if isinstance(command["var_2"], int):
                    state[command["var_1"]] *= command["var_2"]
                else:
                    state[command["var_1"]] *= state[command["var_2"]]
            case "div":
                if isinstance(command["var_2"], int):
                    state[command["var_1"]] //= command["var_2"]
                else:
                    state[command["var_1"]] //= state[command["var_2"]]
            case "mod":
                if isinstance(command["var_2"], int):
                    state[command["var_1"]] %= command["var_2"]
                else:
                    state[command["var_1"]] %= state[command["var_2"]]
            case "eql":
                if isinstance(command["var_2"], int):
                    state[command["var_1"]] = (
                        1 if state[command["var_1"]] == command["var_2"] else 0
                    )
                else:
                    state[command["var_1"]] = (
                        1 if state[command["var_1"]] == state[command["var_2"]] else 0
                    )
            case _:
                raise Exception("Invalid command")

    return state


if __name__ == "__main__":
    print(
        "WARNING: This was only used for verification, and is not a solution to the problem - the included excel was used instead"
    )

    monad = parse_program("input.txt")
    print(run_program(monad, [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]))
    print(run_program(monad, [9, 2, 9, 6, 9, 5, 9, 3, 4, 9, 7, 9, 9, 2]))
    print(run_program(monad, [8, 1, 5, 1, 4, 1, 7, 1, 1, 6, 1, 3, 8, 1]))
