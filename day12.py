from functools import cache
from itertools import product

import day12


@cache
def find_hash_groups(input_string: str) -> list[tuple[int, int]]:
    groups = []
    current_group_start = None

    for i, char in enumerate(input_string):
        if char == '#':
            if current_group_start is None:
                current_group_start = i
        else:
            if current_group_start is not None:
                group_length = i - current_group_start
                groups.append((current_group_start, group_length))
                current_group_start = None

    # Check if the last group extends to the end of the string
    if current_group_start is not None:
        group_length = len(input_string) - current_group_start
        groups.append((current_group_start, group_length))

    return groups


@cache
def check_arrangement(spring_text: str, groups: tuple[int]) -> tuple[bool, str | None]:
    hash_groups: list[tuple[int, int]] = find_hash_groups(spring_text)

    for index, hash_group in enumerate(hash_groups):
        hash_group_start, hash_group_length = hash_group
        if index >= len(groups):
            subtext = spring_text[:hash_group_start + hash_group_length]
            return False, subtext
        if index == len(hash_groups) - 1 and (index + 1) < len(groups):
            subtext = spring_text[:hash_group_start + hash_group_length]
            return False, subtext
        if hash_group_length != groups[index]:
            subtext = spring_text[:hash_group_start + hash_group_length]
            return False, subtext
    return True, None


@cache
def get_arrangements_number(spring_text: str, groups: tuple[int]):
    all_variants: list[str] = []

    # Find all indices of '?'
    question_mark_indices = [i for i, char in enumerate(spring_text) if char == '?']

    # Generate all combinations of '.' and '#'
    combinations = list(product(['.', '#'], repeat=len(question_mark_indices)))

    # Iterate through each combination and replace '?' in the input string
    while combinations:
        combination = combinations.pop()

        variant = list(spring_text)
        for index, replacement in zip(question_mark_indices, combination):
            variant[index] = replacement
        candidate = ''.join(variant)

        check_ok, subtext = check_arrangement(candidate, groups)
        if check_ok:
            all_variants.append(candidate)
        else:
            combination_start = []
            for mark_index in question_mark_indices:
                if mark_index < len(subtext):
                    combination_start.append(subtext[mark_index])
                else:
                    break
            init_count = len(combinations)
            for combination in reversed(combinations):
                if list(combination[:len(combination_start)]) == combination_start:
                    combinations.remove(combination)
            final_count = len(combinations)
            diff = init_count - final_count
            # print(f"Removed {diff} combinations")

    arrangements_count = 0
    while all_variants:
        text = all_variants.pop()
        check_ok, subtext = check_arrangement(text, groups)
        if check_ok:
            arrangements_count += 1
    return arrangements_count


@cache
def calc_total_arrangements(spring_tuple: str, groups_tuple: tuple[int], current_hash_group_length=0):
    if not spring_tuple:
        if current_hash_group_length:
            if len(groups_tuple) == 1 and current_hash_group_length == groups_tuple[0]:
                # correct variation
                return 1
            # incorrect variation
            return 0
        else:
            if len(groups_tuple) == 0:
                # correct variation
                return 1
            # incorrect variation
            return 0

    if current_hash_group_length:
        if not groups_tuple or current_hash_group_length > groups_tuple[0]:
            # in the middle of a hash group despite not expecting one or not expected that length
            return 0

    if spring_tuple[0] == '.':
        if current_hash_group_length:
            # before this, a hash group was found
            if current_hash_group_length != groups_tuple[0]:
                # hash group length doesn't match the expected length
                return 0
            else:
                # hash group length matches the expected length; moving forward
                groups_tuple = groups_tuple[1:]
        return calc_total_arrangements(spring_tuple[1:], groups_tuple, 0)
    elif spring_tuple[0] == '#':
        return calc_total_arrangements(spring_tuple[1:], groups_tuple, current_hash_group_length + 1)
    else:
        # this is ? and can be either . either #
        if not groups_tuple:
            # it can't be # as there are no more hashes expected. Move forward considering here is .
            return calc_total_arrangements(spring_tuple[1:], groups_tuple[1:], 0)
        elif current_hash_group_length == groups_tuple[0]:
            # The current hash group length matches the expected length. Move forward considering here is .
            return calc_total_arrangements(spring_tuple[1:], groups_tuple[1:], 0)
        else:
            # more hash groups still expected and the current hash group length doesn't match the expected length. Move forward considering here is #
            if current_hash_group_length:
                # before ch was #, so the current hash group length is at least 1. Move forward considering here is #
                return calc_total_arrangements(spring_tuple[1:], groups_tuple, current_hash_group_length + 1)
            else:
                # moving forward in 2 directions: considering here is # and considering here is .
                return calc_total_arrangements(spring_tuple[1:], groups_tuple, current_hash_group_length + 1) + calc_total_arrangements(spring_tuple[1:], groups_tuple, current_hash_group_length)


def solve_challenge(input_str: str):
    spring_details: list[tuple[str, tuple[int]]] = []

    for line in input_str.splitlines():
        spring_text: str = line.split(" ")[0].strip()
        groups: tuple[int] = tuple(map(int, list(line.split(" ")[1].strip().split(","))))
        spring_details.append((spring_text, groups))

    print("Solving Part 1")
    # for index, springs_row in enumerate(spring_details):
    #     print(f"Spring {index + 1}: {springs_row}")

    arrangements_list = [get_arrangements_number(spring[0], spring[1]) for spring in spring_details]
    arrangements_sum = sum(arrangements_list)
    print(f"(Part 1) {arrangements_sum=}")

    # part 2

    print("Solving Part 2")
    arrangements_part2_list = []
    for row in spring_details:
        springs_text, spring_number = row
        spring_text = '?'.join([springs_text for _ in range(5)])
        spring_numbers = spring_number * 5
        arrangements_part2_list.append(calc_total_arrangements(spring_tuple=spring_text, groups_tuple=spring_numbers))
        # print(f"For spring row (part2) {springs_text} there are {arrangements_part2_list[-1]} arrangements")

    arrangements_sum_part2 = sum(arrangements_part2_list)
    print(f"(Part2) {arrangements_sum_part2=}")


if __name__ == '__main__':
    print("Demo input")
    solve_challenge(day12.demoinput)

    print()
    print()
    print("Game input")
    solve_challenge(day12.gameinput)
