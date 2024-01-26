import copy

import day10

pipes: dict = {'|': ['north', 'south'],
               '-': ['west', 'east'],
               'L': ['north', 'east'],
               'J': ['north', 'west'],
               '7': ['west', 'south'],
               'F': ['south', 'east'],
               'S': ['north', 'south', 'west', 'east']}

curated_map: list[list[str]] = []


def oposite_cardinal(cardinal: str) -> str:
    if cardinal == 'north':
        return 'south'
    elif cardinal == 'south':
        return 'north'
    elif cardinal == 'east':
        return 'west'
    elif cardinal == 'west':
        return 'east'


def can_be_connected(next_pipe: str, curr_to: str) -> bool:
    if next_pipe == '.':
        return False
    next_pipe_from: str = oposite_cardinal(curr_to)
    next_pipe_cardinals: list[str] = pipes[next_pipe]
    return next_pipe_from in next_pipe_cardinals


def is_valid_pipe(candidate_pipe: str, north_pipe: str | None, south_pipe: str | None, west_pipe: str | None, east_pipe: str | None) -> bool:
    if candidate_pipe not in pipes.keys():
        return False

    pipe_connections = pipes[candidate_pipe]
    candidate_neighbours: list[tuple[str, str]] = []

    for pipe_connection in pipe_connections:
        if pipe_connection == 'north':
            if not north_pipe:
                return False
            else:
                candidate_neighbours.append((north_pipe, 'north'))
        elif pipe_connection == 'south':
            if not south_pipe:
                return False
            else:
                candidate_neighbours.append((south_pipe, 'south'))
        elif pipe_connection == 'west':
            if not west_pipe:
                return False
            else:
                candidate_neighbours.append((west_pipe, 'west'))
        elif pipe_connection == 'east':
            if not east_pipe:
                return False
            else:
                candidate_neighbours.append((east_pipe, 'east'))

    for candidate_neighbour, curr_cardinal_to in candidate_neighbours:
        if not can_be_connected(candidate_neighbour, curr_cardinal_to):
            return False
    return True


def follow_loop(pipe: tuple[str, int, int], direction: str, pipes_order: list):
    stop = False

    pipe_to_process: tuple[str, int, int] = pipe
    pipe_to_process_origin: str = direction
    while not stop:
        # print(f"Processing {pipe_to_process=}")
        if not pipe_to_process:
            pipes_order = None
            break
        this_pipe_type, this_pipe_row, this_pipe_col = pipe_to_process

        if this_pipe_type == '.':
            pipes_order = None
            break

        if this_pipe_type == 'S':
            pipes_order.append(pipe_to_process)
            break

        next_direction = pipes[this_pipe_type][0] if pipes[this_pipe_type][0] != pipe_to_process_origin else pipes[this_pipe_type][1]
        next_pipe_row: int = 0
        next_pipe_col: int = 0
        if next_direction == 'north':
            next_pipe_row = this_pipe_row - 1
            next_pipe_col = this_pipe_col
        elif next_direction == 'south':
            next_pipe_row = this_pipe_row + 1
            next_pipe_col = this_pipe_col
        elif next_direction == 'west':
            next_pipe_row = this_pipe_row
            next_pipe_col = this_pipe_col - 1
        elif next_direction == 'east':
            next_pipe_row = this_pipe_row
            next_pipe_col = this_pipe_col + 1

        if next_pipe_row < 0 or next_pipe_col < 0:
            pipes_order = None
            break
        if next_pipe_row >= len(curated_map) or next_pipe_col >= len(curated_map[0]):
            pipes_order = None
            break

        if not can_be_connected(curated_map[next_pipe_row][next_pipe_col], next_direction):
            pipes_order = None
            break

        pipes_order.append(pipe_to_process)
        pipe_to_process = (curated_map[next_pipe_row][next_pipe_col], next_pipe_row, next_pipe_col)
        pipe_to_process_origin = oposite_cardinal(next_direction)


def sub(from_cell: tuple[int, int], to_cell: tuple[int, int]) -> tuple[int, int]:
    return to_cell[0] - from_cell[0], to_cell[1] - from_cell[1]


def turn_right(direction: tuple[int, int]) -> tuple[int, int]:
    return direction[1], -direction[0]


def turn_left(direction: tuple[int, int]) -> tuple[int, int]:
    return -direction[1], direction[0]


def turn_dir(previous_dir, direction):
    if direction == turn_right(previous_dir):
        return 1
    elif direction == turn_left(previous_dir):
        return -1
    else:
        return 0


def add(cell, direction):
    return cell[0] + direction[0], cell[1] + direction[1]


class map_context:
    def __init__(self, new_map: list[list[str]], full_loop: list[tuple[str, int, int]]):
        self.new_map = new_map
        self.flood_map = [[0 for _ in range(len(new_map[0]))] for _ in range(len(new_map))]
        for current_cell in full_loop:
            self.flood_map[current_cell[1]][current_cell[2]] = 1
        self.chris_flood_map = copy.deepcopy(self.flood_map)
        self.full_loop = full_loop

        row_str = ' '.join([str(index % 10) for index in range(len(self.new_map[0]))])
        print(f"_____ {row_str}")

        for index, row in enumerate(self.new_map):
            row_str = ' '.join(map(str, row))
            print(f"{str(index).zfill(5)} {row_str}")

    def is_border(self, x_start, y_start):
        for element in self.full_loop:
            if element[1] == x_start and element[2] == y_start:
                return True

    def print_flood_map(self, chrismap=False):
        row_str = ' '.join([str(index % 10) for index in range(len(self.flood_map[0]))])
        print(f"_____ {row_str}")

        map_to_print = self.flood_map if not chrismap else self.chris_flood_map
        for index, row in enumerate(map_to_print):
            row_str = ' '.join(map(str, row))
            print(f"{str(index).zfill(5)} {row_str}")

    def part2(self):
        print("Solve part 2")
        # print("Printing flood map")
        # self.print_flood_map()

        previous_one_cell = (self.full_loop[-1][1], self.full_loop[-1][2])
        previous_two_cell = (self.full_loop[-2][1], self.full_loop[-2][2])
        previous_dir = sub(previous_two_cell, previous_one_cell)

        for cell in self.full_loop:
            current_cell = (cell[1], cell[2])
            direction = sub(previous_one_cell, current_cell)
            turn_type = turn_dir(previous_dir, direction)

            candidate_cells = []
            if turn_type == 0:
                # straight
                candidate_cells.append(add(previous_one_cell, turn_right(direction)))
            elif turn_type == -1:
                # left turn
                candidate_cells.append(add(previous_one_cell, turn_right(direction)))
                candidate_cells.append(add(previous_one_cell, turn_right(turn_right(direction))))
                candidate_cells.append(add(add(previous_one_cell, turn_right(direction)), turn_right(turn_right(direction))))
            else:
                # right turn
                pass

            modified = False
            for candidate_cell in candidate_cells:
                in_loop = False
                for loop_cell in self.full_loop:
                    if loop_cell[1] == candidate_cell[0] and loop_cell[2] == candidate_cell[1]:
                        in_loop = True
                        break
                if not in_loop:
                    if 0 <= candidate_cell[0] < len(self.flood_map) and 0 <= candidate_cell[1] < len(self.flood_map[0]):
                        self.flood_map[candidate_cell[0]][candidate_cell[1]] = 2
                        modified = True

            # if modified:
            #     self.print_flood_map()
            #     print()
            #     print()

            previous_two_cell = previous_one_cell
            previous_one_cell = current_cell
            previous_dir = sub(previous_two_cell, previous_one_cell)

        self.print_flood_map()
        print(f"Started to flood fill")
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        updated = True
        while updated:
            updated = False
            for row in range(len(self.flood_map)):
                for col in range(len(self.flood_map[0])):
                    flood_cell = self.flood_map[row][col]
                    if flood_cell == 2:
                        for direction in directions:
                            candidate_flood_cell = add((row, col), direction)
                            if 0 <= candidate_flood_cell[0] < len(self.flood_map) and 0 <= candidate_flood_cell[1] < len(self.flood_map[0]):
                                if self.flood_map[candidate_flood_cell[0]][candidate_flood_cell[1]] == 0:
                                    self.flood_map[candidate_flood_cell[0]][candidate_flood_cell[1]] = 2
                                    updated = True

        flood_cell_count = 0
        for row in self.flood_map:
            flood_cell_count += row.count(2)

        self.print_flood_map()

        print(f"Number of cells filled is {flood_cell_count}")

        for row_index, row in enumerate(self.chris_flood_map):
            for col_index, cell in enumerate(row):
                if cell == 0:
                    # border_numer = list(row[:col_index]).count(1)
                    border_numer = sum([1 for loop_element in self.full_loop if loop_element[1] == row_index and loop_element[2] < col_index and loop_element[0] == '|'])
                    if border_numer % 2 != 0:
                        # vertical_travel = sum([1 for loop_element in self.full_loop if loop_element[1] == row_index and loop_element[2] < col_index and loop_element[0] == '-'])
                        # if (border_numer-vertical_travel) % 2 != 0:
                        self.chris_flood_map[row_index][col_index] = 2

        self.print_flood_map(chrismap=True)
        flood_cell_count = 0
        for row in self.chris_flood_map:
            flood_cell_count += row.count(2)

        print(f"Number of cells filled is {flood_cell_count}")

        for row_index, row in enumerate(self.chris_flood_map):
            for col_index, cell in enumerate(row):
                if cell != self.flood_map[row_index][col_index]:
                    print(f"Difference at {row_index}, {col_index}. Correct flood map has {self.flood_map[row_index][col_index]} and chris flood map has {cell}")
                    break


def solve_challenge(input_str: str):
    print("Solve part 1")

    pipe_map = [list(line.strip()) for line in input_str.splitlines()]

    for row_index, row in enumerate(pipe_map):
        curated_row: list[str] = []
        for col_index, candidate_pipe in enumerate(row):
            north_pipe: str | None = pipe_map[row_index - 1][col_index] if row_index != 0 else None
            south_pipe: str | None = pipe_map[row_index + 1][col_index] if row_index != len(pipe_map) - 1 else None
            west_pipe: str | None = pipe_map[row_index][col_index - 1] if col_index != 0 else None
            east_pipe: str | None = pipe_map[row_index][col_index + 1] if col_index != len(row) - 1 else None

            curated_row.append(candidate_pipe if candidate_pipe in ['S', '.'] or is_valid_pipe(candidate_pipe, north_pipe, south_pipe, west_pipe, east_pipe) else '.')
        curated_map.append(curated_row)

    # print("Curated map: ")
    # for row in clean_map:
    #     print(row)

    S_row_index: int = 0
    S_col_index: int = 0

    for row_index, row in enumerate(curated_map):
        for col_index, pipe in enumerate(row):
            if pipe == 'S':
                S_row_index = row_index
                S_col_index = col_index
                break

    S_west_pipe: tuple[str, int, int] | None = None
    S_east_pipe: tuple[str, int, int] | None = None
    S_north_pipe: tuple[str, int, int] | None = None
    S_south_pipe: tuple[str, int, int] | None = None

    if S_row_index != 0:
        S_north_pipe = (curated_map[S_row_index - 1][S_col_index], S_row_index - 1, S_col_index) if curated_map[S_row_index - 1][S_col_index] != '.' else None
    if S_row_index != len(curated_map) - 1:
        S_south_pipe = (curated_map[S_row_index + 1][S_col_index], S_row_index + 1, S_col_index) if curated_map[S_row_index + 1][S_col_index] != '.' else None
    if S_col_index != 0:
        S_west_pipe = (curated_map[S_row_index][S_col_index - 1], S_row_index, S_col_index - 1) if curated_map[S_row_index][S_col_index - 1] != '.' else None
    if S_col_index != len(curated_map[0]) - 1:
        S_east_pipe = (curated_map[S_row_index][S_col_index + 1], S_row_index, S_col_index + 1) if curated_map[S_row_index][S_col_index + 1] != '.' else None

    go_to_west_loop_length: int = 0
    go_to_east_loop_length: int = 0
    go_to_north_loop_length: int = 0
    go_to_south_loop_length: int = 0
    west_loop: list[tuple[str, int, int]] = []
    east_loop: list[tuple[str, int, int]] = []
    north_loop: list[tuple[str, int, int]] = []
    south_loop: list[tuple[str, int, int]] = []

    if S_west_pipe:
        print()
        print()
        print(f"Heading west")
        pipes_order = []
        follow_loop(S_west_pipe, direction=oposite_cardinal('west'), pipes_order=pipes_order)
        west_loop = pipes_order
        go_to_west_loop_length = len(pipes_order) if pipes_order else None
    if S_east_pipe:
        print()
        print()
        print(f"Heading east")
        pipes_order = []
        follow_loop(S_east_pipe, direction=oposite_cardinal('east'), pipes_order=pipes_order)
        east_loop = pipes_order
        go_to_east_loop_length = len(pipes_order) if pipes_order else None
    if S_north_pipe:
        print()
        print()
        print(f"Heading north")
        pipes_order = []
        follow_loop(S_north_pipe, direction=oposite_cardinal('north'), pipes_order=pipes_order)
        north_loop = pipes_order
        go_to_north_loop_length = len(pipes_order) if pipes_order else None
    if S_south_pipe:
        print()
        print()
        print(f"Heading south")
        pipes_order = []
        follow_loop(S_south_pipe, direction=oposite_cardinal('south'), pipes_order=pipes_order)
        south_loop = pipes_order
        go_to_south_loop_length = len(pipes_order) if pipes_order else None

    print(f"Go to west loop length is {go_to_west_loop_length}")
    print(f"Go to east loop length is {go_to_east_loop_length}")
    print(f"Go to north loop length is {go_to_north_loop_length}")
    print(f"Go to south loop length is {go_to_south_loop_length}")

    print(f"farthest point is {max(go_to_west_loop_length, go_to_east_loop_length, go_to_north_loop_length, go_to_south_loop_length) / 2}")

    context = map_context(new_map=copy.deepcopy(curated_map), full_loop=north_loop)
    context.part2()

    cells_filled = 0

    for row in context.new_map:
        for cell in row:
            if cell == '2':
                cells_filled += 1

    print(f"Cells filled are {cells_filled}")


if __name__ == '__main__':
    # solve_challenge(day10.demoinput_1)
    # solve_challenge(day10.demoinput_2)

    solve_challenge(day10.gameinput)
    # solve_challenge(day10.demoinput_3)
