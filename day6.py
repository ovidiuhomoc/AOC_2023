import math
import sys

import day6
import utils


def compute_ways_to_win(distance, time):
    # print(f"{time} {distance}")

    root1: float = (time + math.sqrt(time ** 2 - 4 * distance)) / 2
    root2: float = (time - math.sqrt(time ** 2 - 4 * distance)) / 2
    in_between_roots = (root1 + root2) / 2
    if (in_between_roots ** 2 - (time * in_between_roots) + distance) > 0:
        raise RuntimeError(f"Test failed: {in_between_roots ** 2 - (time * in_between_roots) + distance} > 0 for {time=}, {distance=}, {root1=}, {root2=}, {in_between_roots=}")

    first_root: float = root1 if root1 <= root2 else root2
    second_root: float = root2 if root1 <= root2 else root1

    first_int_root: int = int(first_root) if int(first_root) > first_root else int(first_root) + 1
    second_int_root: int = int(second_root) if int(second_root) < second_root else int(second_root) - 1

    ways_to_win: int = second_int_root - first_int_root + 1
    print(f"Number of ways to win: {ways_to_win} for {time=}, {distance=}, {root1=}, {root2=}, {in_between_roots=}, {first_root=}, {second_root=}, {first_int_root=}, {second_int_root=}")
    return ways_to_win


def part_1(time_list: list[int], distance_list: list[int]):
    way_to_win_list: list = []

    for index, time in enumerate(time_list):
        distance: int = distance_list[index]
        try:
            ways_to_win = compute_ways_to_win(distance, time)
        except RuntimeError as e:
            print(f"Issue in root calculation for {time=}, {distance=}. {e=}")
            sys.exit(1)
        way_to_win_list.append(ways_to_win)

    # product of all ways to win
    product: int = 1
    for ways_to_win in way_to_win_list:
        product *= ways_to_win

    print(f"Product of all ways to win: {product}")


def part_2(time_list: list[int], distance_list: list[int]):
    new_time = ''.join(map(str, time_list))
    new_time_list: list[int] = [int(new_time)]
    new_distance = ''.join(map(str, distance_list))
    new_distance_list: list[int] = [int(new_distance)]
    part_1(new_time_list, new_distance_list)


if __name__ == '__main__':
    # input_str = day6.demoinput
    input_str = day6.gameinput

    time_list: list[int] = utils.string_utils.to_int_list(input_str.splitlines()[0].split('Time:')[1])
    distance_list: list[int] = utils.string_utils.to_int_list(input_str.splitlines()[1].split('Distance:')[1])

    part_1(time_list, distance_list)
    part_2(time_list, distance_list)
