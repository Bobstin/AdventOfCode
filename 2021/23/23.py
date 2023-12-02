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
WIN_POD = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
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
    for index, room in enumerate(rooms):
        for spot in room:
            if spot != WIN_POD[index]:
                return False

    return True


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

    # Room cannot contain any incorrect pods
    found_incorrect_pod = False
    for spot in rooms[target_room]:
        if spot != pod and spot is not None:
            found_incorrect_pod = True
            break

    # If room is fully empty, or if the first slot is empty and the second has the right pod in it
    if not found_incorrect_pod:
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
            # Find the deepest you can go
            target_room = rooms[TARGET_ROOMS[pod]]
            target_position = None
            for spot_index, spot in enumerate(target_room):
                if spot is None:
                    target_position = spot_index
                else:
                    break

            return [
                {
                    "pod": pod,
                    "from": {"type": "hallway", "index": index},
                    "to": {
                        "type": "room",
                        "index": TARGET_ROOMS[pod],
                        "position": target_position,
                    },
                }
            ]

    # Then rooms
    possible_room_exits = []
    for index, room in enumerate(rooms):
        # If no one in room, skip
        pod = None
        room_position = None
        for spot_index, spot in enumerate(room):
            if spot is not None:
                pod = spot
                room_position = spot_index
                break
        if pod is None:
            continue

        # If you can't leave the room, skip
        exit = ROOM_EXITS[index]
        if hallway[exit] is not None:
            continue

        # If everyone in the room is correct, skip
        if all([spot == WIN_POD[index] for spot in room]):
            continue

        # If you are in the back of the target room, skip
        last_room_position = len(room) - 1
        if room_position == last_room_position and TARGET_ROOMS[pod] == index:
            continue

        # Get the farthest back spot available in the target room
        farthest_back_available = None
        for position_index in range(last_room_position, -1, -1):
            if rooms[TARGET_ROOMS[pod]][position_index] is None:
                farthest_back_available = position_index
                break

        # If you are in the front of the target room and the back is empty, go to the back
        if (
            room_position < last_room_position
            and TARGET_ROOMS[pod] == index
            and farthest_back_available is not None
            and farthest_back_available > room_position
        ):
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
                        "position": farthest_back_available,
                    },
                }
            ]

        # Otherwise, if you are in the target room already and everything behind you is correct, skip
        if TARGET_ROOMS[pod] == index:
            all_others_correct = True
            for position_index in range(room_position, len(room)):
                if room[position_index] != pod:
                    all_others_correct = False
                    break
            if all_others_correct:
                continue

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
                        "position": farthest_back_available,
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
    adjusted_rooms = []
    for room in rooms:
        adjusted_rooms.append([pod if pod is not None else "None" for pod in room])
    return (
        "HW: "
        + "".join(adjusted_hallway)
        + " RM:"
        + "".join([f"[{','.join(room)}]" for room in adjusted_rooms])
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
    test_initial_rooms = [
        ["B", "D", "D", "A"],
        ["C", "C", "B", "D"],
        ["B", "B", "A", "C"],
        ["D", "A", "C", "A"],
    ]
    min_energy = None
    achieved_states = {}
    play(initial_hallway, test_initial_rooms, 0, [])
    print(min_energy)

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
    initial_rooms = [
        ["D", "D", "D", "C"],
        ["B", "C", "B", "C"],
        ["B", "B", "A", "D"],
        ["A", "A", "C", "A"],
    ]
    min_energy = None
    achieved_states = {}
    play(initial_hallway, initial_rooms, 0, [])
    print(min_energy)
