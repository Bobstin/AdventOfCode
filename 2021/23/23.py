ROOM_EXITS = {
    0: 2,
    1: 4,
    2: 6,
    3: 8,
}
TARGET_ROOMS = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
}
DIFFICULTY = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}

min_energy = None
achieved_states: dict[str, int] = {}


# Can't move from first spot in hallway unless second spot in hallway is empty
# If possible to move to target room (and not block someone in), should always do so
# If not possible to move to target room, should move to empty spot in hallway
def play(hallway, rooms, energy, prior_moves):
    global min_energy
    global achieved_states

    hashed_state = hash_state(hallway, rooms)
    if hashed_state in achieved_states and energy >= achieved_states[hashed_state]:
        return

    achieved_states[hashed_state] = energy

    # If we are higher energy than a success, stop
    if min_energy is not None and energy >= min_energy:
        return

    # If we are in a winning state, stop
    if check_for_win(rooms):
        min_energy = energy
        return

    # Otherwise, get the possible moves
    moves = possible_moves(hallway, rooms)

    # If no possible moves, return
    if len(moves) == 0:
        return

    # Otherwise, try each move
    for move in moves:
        # Make a copy of the hallway and rooms
        new_hallway = hallway.copy()
        new_rooms = [room.copy() for room in rooms]

        # Remove the pod from the old location
        if move["from"]["type"] == "hallway":
            new_hallway[move["from"]["index"]] = None
        else:
            new_rooms[move["from"]["index"]][move["from"]["position"]] = None

        # Add the pod to the new location
        if move["to"]["type"] == "hallway":
            new_hallway[move["to"]["index"]] = move["pod"]
        else:
            new_rooms[move["to"]["index"]][move["to"]["position"]] = move["pod"]

        # Recurse
        energy_used = score_move(move)
        new_prior_moves = [move.copy() for move in prior_moves] + [move]
        play(new_hallway, new_rooms, energy + energy_used, new_prior_moves)


def check_for_win(rooms):
    return (
        rooms[0][0] == "A"
        and rooms[0][1] == "A"
        and rooms[1][0] == "B"
        and rooms[1][1] == "B"
        and rooms[2][0] == "C"
        and rooms[2][1] == "C"
        and rooms[3][0] == "D"
        and rooms[3][1] == "D"
    )


def check_for_ability_to_reach_target(
    pod: str,
    hallway: list[str | None],
    starting_pos: int,
    rooms: list[list[str | None]],
) -> tuple[bool, list[int]]:
    possible_hallways = []
    # Try going left
    current_pos = starting_pos - 1
    while current_pos >= 0:
        if hallway[current_pos] is None:
            possible_hallways.append(current_pos)
            current_pos -= 1
        else:
            break

    # Try going right
    current_pos = starting_pos + 1
    while current_pos < len(hallway):
        if hallway[current_pos] is None:
            possible_hallways.append(current_pos)
            current_pos += 1
        else:
            break

    # Figure out where they want to go
    target_room = TARGET_ROOMS[pod]
    target_room_exit = ROOM_EXITS[target_room]

    # If room is fully empty, or if the first slot is empty and the second has the right pod in it
    if (rooms[target_room][0] is None and rooms[target_room][1] is None) or (
        rooms[target_room][0] is None and rooms[target_room][1] == pod
    ):
        # If it is, see if they can get there
        if target_room_exit < starting_pos:
            required_clear_hallway = set(range(target_room_exit, starting_pos))
        else:
            required_clear_hallway = set(range(starting_pos + 1, target_room_exit + 1))

        # If it is possible then go there
        if required_clear_hallway.issubset(set(possible_hallways)):
            return True, possible_hallways

    return False, possible_hallways


def possible_moves(
    hallway: list[str | None], rooms: list[list[str | None]]
) -> list[dict]:
    # Start with hallways
    for index, pod in enumerate(hallway):
        if pod is None:
            continue

        can_make_room, possible_hallways = check_for_ability_to_reach_target(
            pod, hallway, index, rooms
        )
        if can_make_room:
            return [
                {
                    "pod": pod,
                    "from": {"type": "hallway", "index": index},
                    "to": {
                        "type": "room",
                        "index": TARGET_ROOMS[pod],
                        "position": 1 if rooms[TARGET_ROOMS[pod]][1] is None else 0,
                    },
                }
            ]

    # Then rooms
    possible_room_exits = []
    for index, room in enumerate(rooms):
        # If no one in room, skip
        if room[0] is None and room[1] is None:
            continue

        # If you can't leave the room, skip
        exit = ROOM_EXITS[index]
        if hallway[exit] is not None:
            continue

        pod = room[0] if room[0] is not None else room[1]
        assert pod is not None
        room_position = 0 if room[0] is not None else 1

        # If you are in the back of the target room, skip
        if room_position == 1 and TARGET_ROOMS[pod] == index:
            continue

        # If you are in the front of the target room and the back is empty, go to the back
        if room_position == 0 and TARGET_ROOMS[pod] == index and room[1] is None:
            return [
                {
                    "pod": pod,
                    "from": {
                        "type": "room",
                        "index": index,
                        "position": room_position,
                    },
                    "to": {
                        "type": "room",
                        "index": index,
                        "position": 1,
                    },
                }
            ]

        can_make_room, possible_hallways = check_for_ability_to_reach_target(
            pod, hallway, exit, rooms
        )

        # If it is possible then go there
        if can_make_room:
            return [
                {
                    "pod": pod,
                    "from": {
                        "type": "room",
                        "index": index,
                        "position": room_position,
                    },
                    "to": {
                        "type": "room",
                        "index": TARGET_ROOMS[pod],
                        "position": 1 if rooms[TARGET_ROOMS[pod]][1] is None else 0,
                    },
                }
            ]
        else:
            possible_room_exits += [
                {
                    "pod": pod,
                    "from": {
                        "type": "room",
                        "index": index,
                        "position": room_position,
                    },
                    "to": {"type": "hallway", "index": hallway_index},
                }
                for hallway_index in possible_hallways
                if hallway_index not in ROOM_EXITS.values()
            ]
    return possible_room_exits


def score_move(move: dict) -> int:
    # Shortcut if just moving within a room
    if (
        move["from"]["type"] == "room"
        and move["to"]["type"] == "room"
        and move["from"]["index"] == move["to"]["index"]
    ):
        return abs(move["to"]["position"] - move["from"]["position"])

    if move["from"]["type"] == "room":
        hallway_start = ROOM_EXITS[move["from"]["index"]]
        room_steps_start = move["from"]["position"] + 1
    else:
        hallway_start = move["from"]["index"]
        room_steps_start = 0

    if move["to"]["type"] == "room":
        hallway_end = ROOM_EXITS[move["to"]["index"]]
        room_steps_end = move["to"]["position"] + 1
    else:
        hallway_end = move["to"]["index"]
        room_steps_end = 0

    total_steps = abs(hallway_start - hallway_end) + room_steps_start + room_steps_end
    difficulty = DIFFICULTY[move["pod"]]

    move["steps"] = total_steps
    move["difficulty"] = difficulty
    move["energy"] = total_steps * difficulty

    return total_steps * difficulty


def hash_state(hallway, rooms):
    adjusted_hallway = [pod if pod is not None else "None" for pod in hallway]
    return (
        "HW: "
        + "".join(adjusted_hallway)
        + " RM:"
        + "".join(
            [
                f"[{room[0] if room[0] is not None else 'None'},{room[1] if room[1] is not None else 'None'}]"
                for room in rooms
            ]
        )
    )


if __name__ == "__main__":
    test_initial_hallway = [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    test_initial_rooms = [["B", "A"], ["C", "D"], ["B", "C"], ["D", "A"]]
    min_energy = None
    play(test_initial_hallway, test_initial_rooms, 0, [])
    print(min_energy)
    assert min_energy == 12521

    initial_hallway = [
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
    initial_rooms = [["D", "C"], ["B", "C"], ["B", "D"], ["A", "A"]]
    min_energy = None
    achieved_states = {}
    play(initial_hallway, initial_rooms, 0, [])
    print(min_energy)
