import sys
import time
from functools import cache

import day14


@cache
def rotate_clockwise(rocks_map: list[list[str]]) -> tuple[tuple[str]]:
    rocks_map_copy: list[list[str]] = [list(row) for row in rocks_map]

    new_rocks_map: list[list[str]] = []
    for i in range(len(rocks_map_copy[0])):
        new_rocks_map.append(["" for j in range(len(rocks_map_copy))])

    for row_index, row in enumerate(rocks_map_copy):
        for col_index, cell in enumerate(row):
            new_map_col_index: int = len(rocks_map_copy) - row_index - 1
            new_map_row_index: int = col_index
            new_rocks_map[new_map_row_index][new_map_col_index] = cell

    return tuple(tuple([cell for cell in row]) for row in new_rocks_map)


@cache
def rotate_counter_clockwise(rocks_map: tuple[tuple[str]]) -> tuple[tuple[str]]:
    rocks_map_copy: list[list[str]] = [list(row) for row in rocks_map]

    new_rocks_map: list[list[str]] = []
    for i in range(len(rocks_map_copy[0])):
        new_rocks_map.append(["" for j in range(len(rocks_map_copy))])

    for row_index, row in enumerate(rocks_map_copy):
        for col_index, cell in enumerate(row):
            new_map_col_index: int = row_index
            new_map_row_index: int = len(rocks_map_copy[0]) - col_index - 1
            new_rocks_map[new_map_row_index][new_map_col_index] = cell

    return tuple(tuple([cell for cell in row]) for row in new_rocks_map)


@cache
def move_rock_north(rocks_map: tuple[tuple[str]], row_index: int, col_index: int) -> tuple[tuple[str]]:
    rocks_map_copy: list[list[str]] = [list(row) for row in rocks_map]

    current_row = row_index
    while True:
        above_row = current_row - 1

        if above_row < 0:
            break

        if rocks_map_copy[above_row][col_index] == '#' or rocks_map_copy[above_row][col_index] == 'O':
            break

        above_cell = rocks_map_copy[above_row][col_index]
        rocks_map_copy[above_row][col_index] = 'O'
        rocks_map_copy[current_row][col_index] = above_cell
        current_row = above_row

    return tuple(tuple([cell for cell in row]) for row in rocks_map_copy)


def part1(input_str: str, control: str | None = None):
    rocks_map: list[list[str]] = [list(row) for row in input_str.splitlines()]
    control_map: list[list[str]] = [list(row) for row in control.splitlines()] if control else None

    rocks_map_copy: tuple[tuple[str]] = tuple(tuple(cell for cell in row) for row in rocks_map)

    modified: bool = True
    last_modif_coord: tuple[int, int] = (-1, -1)
    while modified:
        modified = False

        for row_index, row in enumerate(rocks_map_copy):
            if modified:
                break
            for col_index, col in enumerate(row):
                if ((row_index == last_modif_coord[0] and col_index > last_modif_coord[1]) or row_index > last_modif_coord[0]) and col == 'O':
                    rocks_map_copy = move_rock_north(rocks_map_copy, row_index, col_index)
                    modified = True
                    last_modif_coord = (row_index, col_index)
                    break

    # check against the control
    if control:
        different: bool = False

        for row_index, row in enumerate(rocks_map_copy):
            for col_index, col in enumerate(row):
                if col != control_map[row_index][col_index]:
                    print(f'Error at row {row_index}, col {col_index}')
                    print(f'Expected {control_map[row_index][col_index]}, got {col}')
                    different = True

        if not different:
            print('No differences found')
        else:
            for row_index, row in enumerate(rocks_map_copy):
                print(f"{''.join(row)}\t\t\t{''.join(control_map[row_index])}")

    load_sum: int = 0
    for row_index, row in enumerate(rocks_map_copy):
        load_multiplier: int = len(rocks_map_copy) - row_index
        load_sum += row.count('O') * load_multiplier

    print(f'(Part1) Load sum: {load_sum}')


@cache
def tilt_north(rocks_map_copy: tuple[tuple[str]]) -> tuple[tuple[str]]:
    # tilt to north
    modified: bool = True
    last_modif_coord: tuple[int, int] = (-1, -1)
    while modified:
        modified = False

        for row_index, row in enumerate(rocks_map_copy):
            if modified:
                break
            for col_index, col in enumerate(row):
                if ((row_index == last_modif_coord[0] and col_index > last_modif_coord[1]) or row_index > last_modif_coord[0]) and col == 'O':
                    rocks_map_copy = move_rock_north(rocks_map_copy, row_index, col_index)
                    modified = True
                    last_modif_coord = (row_index, col_index)
                    break

    return rocks_map_copy


@cache
def tilt_cardinal(rocks_map_copy: tuple[tuple[str]], cardinal: str) -> tuple[tuple[str]]:
    if cardinal == "north":
        pass
    elif cardinal == "west":
        rocks_map_copy = rotate_clockwise(rocks_map_copy)
    elif cardinal == "south":
        rocks_map_copy = rotate_clockwise(rocks_map_copy)
        rocks_map_copy = rotate_clockwise(rocks_map_copy)
    elif cardinal == "east":
        rocks_map_copy = rotate_counter_clockwise(rocks_map_copy)

    # tilt to north
    modified: bool = True
    last_modif_coord: tuple[int, int] = (-1, -1)
    while modified:
        modified = False

        for row_index, row in enumerate(rocks_map_copy):
            if modified:
                break
            for col_index, col in enumerate(row):
                if ((row_index == last_modif_coord[0] and col_index > last_modif_coord[1]) or row_index > last_modif_coord[0]) and col == 'O':
                    rocks_map_copy = move_rock_north(rocks_map_copy, row_index, col_index)
                    modified = True
                    last_modif_coord = (row_index, col_index)
                    break

    if cardinal == "north":
        pass
    elif cardinal == "west":
        rocks_map_copy = rotate_counter_clockwise(rocks_map_copy)
    elif cardinal == "south":
        rocks_map_copy = rotate_counter_clockwise(rocks_map_copy)
        rocks_map_copy = rotate_counter_clockwise(rocks_map_copy)
    elif cardinal == "east":
        rocks_map_copy = rotate_clockwise(rocks_map_copy)

    return rocks_map_copy


@cache
def complete_cycle(rocks_map_copy: tuple[tuple[str]]) -> tuple[tuple[str]]:
    rocks_map_copy = tilt_north(rocks_map_copy)

    #west
    rocks_map_copy = rotate_clockwise(rocks_map_copy)
    rocks_map_copy = tilt_north(rocks_map_copy)

    #south
    rocks_map_copy = rotate_clockwise(rocks_map_copy)
    rocks_map_copy = tilt_north(rocks_map_copy)

    #east
    rocks_map_copy = rotate_clockwise(rocks_map_copy)
    rocks_map_copy = tilt_north(rocks_map_copy)

    #north
    rocks_map_copy = rotate_clockwise(rocks_map_copy)

    # rocks_map_copy = tilt_cardinal(rocks_map_copy, "north")
    # rocks_map_copy = tilt_cardinal(rocks_map_copy, "west")
    # rocks_map_copy = tilt_cardinal(rocks_map_copy, "south")
    # rocks_map_copy = tilt_cardinal(rocks_map_copy, "east")
    return rocks_map_copy


def print_rocks_map(rocks_map: tuple[tuple[str]]):
    for row_index, row in enumerate(rocks_map):
        print(f"{''.join(row)}")


@cache
def are_maps_equal(map1: tuple[tuple[str]], map2: tuple[tuple[str]]) -> bool:
    for row_index, row in enumerate(map1):
        for col_index, col in enumerate(row):
            if col != map2[row_index][col_index]:
                return False
    return True


def part2(input_str: str):
    start = time.perf_counter()

    rocks_map: list[list[str]] = [list(row) for row in input_str.splitlines()]
    rocks_map_copy: tuple[tuple[str]] = tuple(tuple([cell for cell in row]) for row in rocks_map)

    maps_store: list[tuple[tuple[str]]] = [rocks_map_copy]

    cycles_count: int = 1000000000
    # cycles_count: int = 1000
    # cycles_count: int = 3

    max_prints: int = 104

    for cycle_index in range(cycles_count):
        rocks_map_copy = complete_cycle(rocks_map_copy)

        if max_prints:
            for map_index, map in enumerate(maps_store):
                if are_maps_equal(map, rocks_map_copy):
                    print(f"The map after cycle {cycle_index} is the same as after cycle {map_index}")
                    max_prints -= 1
                    break
            maps_store.append(rocks_map_copy)

            load_sum = get_load_sum(rocks_map_copy)
            print(f'After cycle {cycle_index} the load sum is : {load_sum}')
        else:
            print(f"Printed {max_prints} times, skipping the rest...")
            end = time.perf_counter()
            print(f"Time elapsed: {end - start}")
            sys.exit(0)

    # load_sum: int = 0
    # for row_index, row in enumerate(rocks_map_copy):
    #     load_multiplier: int = len(rocks_map_copy) - row_index
    #     load_sum += row.count('O') * load_multiplier
    #
    # print(f'Load sum: {load_sum}')


@cache
def get_load_sum(rocks_map_copy):
    load_sum: int = 0
    for row_index, row in enumerate(rocks_map_copy):
        load_multiplier: int = len(rocks_map_copy) - row_index
        load_sum += row.count('O') * load_multiplier
    return load_sum


if __name__ == '__main__':
    # print("Demo input")
    # part1(day14.demoinput, day14.democontrol)
    # part2(day14.demoinput)

    print()
    print()
    print("Game input")
    part1(day14.gameinput)
    part2(day14.gameinput)
