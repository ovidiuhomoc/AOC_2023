from functools import wraps

import day11


def print_map(galaxy_map: list[list[str]]):
    row_str = ' '.join([str(index % 10) for index in range(len(galaxy_map[0]))])
    print(f"_____ {row_str}")

    for index, row in enumerate(galaxy_map):
        row_str = ' '.join(map(str, row))
        print(f"{str(index).zfill(5)} {row_str}")


def cache_heuristic(func):
    local_cached_heuristic: dict = {}

    @wraps(func)
    def wrapper(node: tuple[int, int], goal: tuple[int, int]) -> int:
        if (node, goal) not in local_cached_heuristic or (goal, node) not in local_cached_heuristic:
            local_cached_heuristic[(node, goal)] = func(node, goal)
        if (node, goal) in local_cached_heuristic:
            return local_cached_heuristic[(node, goal)]
        else:
            return local_cached_heuristic[(goal, node)]

    return wrapper


@cache_heuristic
def heuristic(node, goal):
    # Manhattan distance heuristic
    x1, y1 = node
    x2, y2 = goal
    return abs(x1 - x2) + abs(y1 - y2)


def build_path(closed_list, selected_node):
    path = []
    while selected_node != 'None':
        path.append(selected_node)
        selected_node = closed_list[selected_node]['parent']
    path.reverse()
    return path


def astar2(matrix, start, goal):
    rows, cols = len(matrix), len(matrix[0])

    open_list: dict = {}
    open_list[start] = 0

    closed_list: dict = {}
    closed_list[start] = {'f_score': 0,
                          'g_score': 0,
                          'h_score': 0,
                          'parent': 'None'}

    while open_list:
        selected_node = None
        selected_f = float('infinity')

        for node, f in open_list.items():
            if f < selected_f:
                selected_node = node
                selected_f = f

        open_list.pop(selected_node)

        successors = []
        successors.append((selected_node[0] - 1, selected_node[1]))
        successors.append((selected_node[0] + 1, selected_node[1]))
        successors.append((selected_node[0], selected_node[1] - 1))
        successors.append((selected_node[0], selected_node[1] + 1))

        for successor in successors:
            if successor == goal:
                path = build_path(closed_list, selected_node)
                return closed_list[selected_node]['g_score'] + 1, path

            if 0 <= successor[0] < rows and 0 <= successor[1] < cols:
                successor_g = closed_list[selected_node]['g_score'] + 1
                successor_h = heuristic(successor, goal)
                successor_f = successor_g + successor_h

                if successor in open_list:
                    if successor_f > open_list[successor]:
                        continue

                if successor in closed_list:
                    if successor_f > closed_list[successor]['f_score']:
                        continue

                open_list[successor] = successor_f
                closed_list[successor] = {'f_score': successor_f,
                                          'g_score': successor_g,
                                          'h_score': successor_h,
                                          'parent': selected_node}


class GalaxyPath:
    def __init__(self, start, end, distance, path):
        self.start = start
        self.end = end
        self.distance = distance
        self.path = path

    def __repr__(self):
        return f"{self.start} -> {self.end} = {self.distance} steps"

    def has_element(self, element):
        return element in self.path


def solve_challenge(input_str: str, multiplier: int = 1):
    compact_galaxy_map: list[list[str]] = [list(row) for row in input_str.splitlines()]

    # print("Before expanding:")
    # print_map(compact_galaxy_map)

    rows_to_expand: list[int] = [index for index, row in enumerate(compact_galaxy_map) if not row.count('#')]

    cols_number = len(compact_galaxy_map[0])
    cols_to_expand: list[int] = [col_index for col_index in range(cols_number) if not any(row[col_index] == '#' for row in compact_galaxy_map)]

    expanded_galaxy_map: list[list[str]] = []
    for row_index, row in enumerate(compact_galaxy_map):
        expanded_row = list("".join(cell * 2 if col_index in cols_to_expand else cell for col_index, cell in enumerate(row)))
        expanded_galaxy_map.extend([expanded_row] if row_index not in rows_to_expand else [expanded_row, expanded_row])

    # print("After expanding:")
    # print_map(expanded_galaxy_map)

    galaxies_coordinates = [(row_index, col_index) for row_index, row in enumerate(expanded_galaxy_map) for col_index, cell in enumerate(row) if cell == '#']
    galaxy_pairs = [(galaxy1_coord, galaxy2_coord) for galaxy_1_index, galaxy1_coord in enumerate(galaxies_coordinates) for galaxy2_coord in galaxies_coordinates[galaxy_1_index + 1:]]
    pairs_distances = [abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1]) for pair in galaxy_pairs]  # each pair manhattan distance  |  abs(start_row - end_row) + abs(start_col - end_col)
    distances_sum = sum(pairs_distances)  # sum of each manhattan distance
    print(f"Solution of part 1 is {distances_sum=}")

    # part 2

    # Solving the part 2 challenge
    compact_galaxies_coordinates = [(row_index, col_index) for row_index, row in enumerate(compact_galaxy_map) for col_index, cell in enumerate(row) if cell == '#']
    compact_galaxy_pairs = [(compact_g1_coord, compact_g2_coord) for compact_g1_index, compact_g1_coord in enumerate(compact_galaxies_coordinates) for compact_g2_coord in compact_galaxies_coordinates[compact_g1_index + 1:]]

    distances_sum_part2 = 0
    for pair in compact_galaxy_pairs:
        start = pair[0]
        end = pair[1]

        star_row, start_col = start
        end_row, end_col = end

        first_row = star_row if star_row < end_row else end_row
        last_row = star_row if star_row > end_row else end_row

        first_col = start_col if start_col < end_col else end_col
        last_col = start_col if start_col > end_col else end_col

        expandable_rows_count = sum(1 for row_index in range(first_row, last_row) if row_index in rows_to_expand)
        expandable_cols_count = sum(1 for col_index in range(first_col, last_col) if col_index in cols_to_expand)

        horiz_distance = abs(star_row - end_row)
        vert_distance = abs(start_col - end_col)
        exp_horiz_distance = horiz_distance - expandable_rows_count + (expandable_rows_count * multiplier)
        exp_vert_distance = vert_distance - expandable_cols_count + (expandable_cols_count * multiplier)
        manhattan_distance = exp_horiz_distance + exp_vert_distance
        # print(f" {start} -> {end} = {distance} steps")
        distances_sum_part2 += manhattan_distance

    print(f" {distances_sum_part2=}")


if __name__ == '__main__':
    print("Demo Input")
    solve_challenge(input_str=day11.demoinput, multiplier=1)
    print()
    solve_challenge(input_str=day11.demoinput, multiplier=10)
    print()
    solve_challenge(input_str=day11.demoinput, multiplier=100)

    print()
    print()
    print("Game Input")
    solve_challenge(input_str=day11.gameinput, multiplier=1000000)
