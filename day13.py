import copy

import day13


def get_line_mirroring_indices(line: list[str], indices: list[int] or None = None) -> list[int]:
    mirrors: list[int] = []

    indices_to_check: list[int] = list(range(1, len(line))) if indices is None else indices

    for col_index in indices_to_check:
        left = line[:col_index]
        right = line[col_index:]

        size_left = len(left)
        size_right = len(right)

        if size_left < size_right:
            right = right[:size_left]
        elif size_right < size_left:
            left = left[-size_right:]

        right = right[::-1]
        if left == right:
            mirrors.append(col_index)

    return mirrors


def get_smudged_coord(matrix: list[list[str]]) -> tuple[int, int]:
    differences_count: list[tuple[int, int, tuple[int, int]]] = []

    for line_index in range(1, len(matrix)):
        diff_count = 0

        top_limit = -1
        bot_limit = len(matrix)

        top_line_index = line_index
        bot_line_index = len(matrix) - line_index

        if top_line_index < bot_line_index:
            bot_limit = 2 * top_line_index
        elif bot_line_index < top_line_index:
            top_limit = len(matrix) - 2 * bot_line_index - 1

        smudge_coords: tuple[int, int] | None = None
        for row_index, row in enumerate(matrix):
            if top_limit < row_index < line_index:
                for col_index, cell in enumerate(row):
                    # a top line
                    curr_char = cell
                    row_of_opposite_char = bot_limit - (row_index - top_limit)
                    opposite_char = matrix[row_of_opposite_char][col_index]
                    if curr_char != opposite_char:
                        diff_count += 1
                        if smudge_coords is None:
                            smudge_coords = (row_index, col_index)

        differences_count.append((line_index, diff_count, smudge_coords))

    for line_index, diff_count, smudge_coords in differences_count:
        if diff_count == 1:
            return smudge_coords


def solve_challenge(input_str: str):
    patterns: list[str] = [pattern + '\n' for pattern in input_str.split('\n\n')]

    pattern_details: dict = {}
    for pattern_index, pattern in enumerate(patterns):
        pattern_copy: list[list[str]] = [list(line) for line in pattern.splitlines()]
        vert_mirroring: list[int] = get_mirroring_details(pattern_copy)

        counter_clockwise_rotated_pattern: list[list[str]] = [[line[col_index] for line in pattern_copy] for col_index in range(len(pattern_copy[0]) - 1, -1, -1)]
        horz_mirroring: list[int] = get_mirroring_details(counter_clockwise_rotated_pattern)

        pattern_details[pattern_index] = {'multi_line_str': pattern,
                                          'matrix': pattern_copy,
                                          'rotated_matrix': counter_clockwise_rotated_pattern,
                                          'vert_mirroring': vert_mirroring,
                                          'horz_mirroring': horz_mirroring}

    total_sum = 0
    for key in pattern_details.keys():
        if pattern_details[key]['vert_mirroring']:
            multiplier = 1
            total_sum += sum(multiplier * mirroring for mirroring in pattern_details[key]['vert_mirroring'])
        if pattern_details[key]['horz_mirroring']:
            multiplier = 100
            total_sum += sum(multiplier * mirroring for mirroring in pattern_details[key]['horz_mirroring'])

    print(f"(Part1) {total_sum=}")

    for pattern_index in pattern_details.keys():
        try:
            coords: tuple[int, int] = get_smudged_coord(pattern_details[pattern_index]['matrix'])
            if coords:
                modified_matrix = copy.deepcopy(pattern_details[pattern_index]['matrix'])
                if modified_matrix[coords[0]][coords[1]] == '#':
                    modified_matrix[coords[0]][coords[1]] = '.'
                else:
                    modified_matrix[coords[0]][coords[1]] = '#'

                counter_clockwise_rotated_pattern: list[list[str]] = [[line[col_index] for line in modified_matrix] for col_index in range(len(modified_matrix[0]) - 1, -1, -1)]
                pattern_details[pattern_index]['modif_matrix'] = counter_clockwise_rotated_pattern
                part2_vert_mirroring: list[int] = get_mirroring_details(counter_clockwise_rotated_pattern)

                pattern_details[pattern_index]['part2_vert_mirroring'] = part2_vert_mirroring
                pattern_details[pattern_index]['part2_vert_mirror_smudge_coords'] = coords
        except Exception as e:
            print(e)
            print(f"{pattern_index=}")
            print(f"{coords=}")
            raise e

        try:
            coords: tuple[int, int] = get_smudged_coord(pattern_details[pattern_index]['rotated_matrix'])
            if coords:
                modified_matrix = copy.deepcopy(pattern_details[pattern_index]['rotated_matrix'])
                if modified_matrix[coords[0]][coords[1]] == '#':
                    modified_matrix[coords[0]][coords[1]] = '.'
                else:
                    modified_matrix[coords[0]][coords[1]] = '#'

                clockwise_rotated_pattern: list[list[str]] = [[line[col_index] for line in reversed(modified_matrix)] for col_index in range(len(modified_matrix[0]))]
                part2_horz_mirroring: list[int] = get_mirroring_details(clockwise_rotated_pattern)

                pattern_details[pattern_index]['part2_horz_mirroring'] = part2_horz_mirroring
                pattern_details[pattern_index]['part2_horz_mirror_smudge_coords'] = coords
        except Exception as e:
            print(e)
            print(f"{pattern_index=}")
            print(f"{coords=}")
            raise e

    part2_sum = 0
    for pattern_index in pattern_details.keys():
        if pattern_details[pattern_index].get('part2_vert_mirroring'):
            multiplier = 100
            part2_sum += sum(multiplier * vert_index for vert_index in pattern_details[pattern_index]['part2_vert_mirroring'] if vert_index not in pattern_details[pattern_index]['horz_mirroring'])

        if pattern_details[pattern_index].get('part2_horz_mirroring'):
            multiplier = 1
            part2_sum += sum(multiplier * horz_index for horz_index in pattern_details[pattern_index]['part2_horz_mirroring'] if horz_index not in pattern_details[pattern_index]['vert_mirroring'])

    print(part2_sum)


def get_mirroring_details(pattern: list[list[str]]) -> list[int]:
    mirror_indices: list[int] = []
    for index, line in enumerate(pattern):
        mirror_indices = get_line_mirroring_indices(line) if index == 0 else get_line_mirroring_indices(line, mirror_indices)
    return mirror_indices


if __name__ == '__main__':
    print("Demo input")
    solve_challenge(day13.demoinput)

    print()
    print()
    print("Game input")
    solve_challenge(day13.gameinput)
