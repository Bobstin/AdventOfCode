import numpy as np
from tqdm import tqdm


def parse_input(file: str) -> tuple[np.ndarray, np.ndarray]:
    with open(file) as f:
        down_array = np.array(
            [
                [1 if char == "v" else 0 for char in line.strip()]
                for line in f.readlines()
            ]
        )
    with open(file) as f:
        right_array = np.array(
            [
                [1 if char == ">" else 0 for char in line.strip()]
                for line in f.readlines()
            ]
        )

    return right_array, down_array


def simulate_step(right: np.ndarray, down: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    # Get the combined map
    combined = right + down
    # print(combined)

    # Shift the world left since we want overlaps of gaps with downs
    left_shifted = np.roll(combined, -1, axis=1)
    # print(left_shifted)

    # Identify who can move - anyone who is a 1 in the right array, and a 0 in the shifted array means they have a gap to their right
    can_move_right = ((right - left_shifted) == 1) * 1

    # Actually do the shift - subtract their current positions, do the shift then add them back
    right = right - can_move_right + np.roll(can_move_right, 1, axis=1)

    # Do the same for the down
    combined = right + down  # Need to do this again, since right is now different
    up_shifted = np.roll(combined, -1, axis=0)
    can_move_down = ((down - up_shifted) == 1) * 1
    down = down - can_move_down + np.roll(can_move_down, 1, axis=0)

    return right, down


def simulate_until_stopped(
    right: np.ndarray, down: np.ndarray
) -> tuple[int, np.ndarray, np.ndarray]:
    num_steps = 0
    with tqdm() as pbar:
        while True:
            right_before_steps = right.copy()
            down_before_steps = down.copy()
            right, down = simulate_step(right, down)
            num_steps += 1
            pbar.update(1)
            if np.all((right_before_steps - right) == 0) and np.all(
                (down_before_steps - down) == 0
            ):
                break

    return num_steps, right, down


if __name__ == "__main__":
    test_right, test_down = parse_input("test_input.txt")
    test_num_steps, test_right, test_down = simulate_until_stopped(
        test_right, test_down
    )
    print(test_num_steps)
    assert test_num_steps == 58

    right, down = parse_input("input.txt")
    steps, right, down = simulate_until_stopped(right, down)
    print(steps)
