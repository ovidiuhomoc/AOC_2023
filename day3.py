import day3

symbol_list = ['*', '/', '+', '-', '(', ')', '!', '@', '#', '$', '%', '^', '&', '~', '`', '|', '\\', '<', '>', '?', ':', ';', ',', '[', ']', '{', '}', '=', '_', '-', '+', '"', "'", ' ']
digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def get_valid_number(prev_line: str, line: str, next_line: str) -> tuple[list, list]:
    candidate_list: list = []
    number_buffer: str = ""

    for index, ch in enumerate(line):
        if ch in digit_list:
            number_buffer += ch
        else:
            if number_buffer != "":
                candidate_list.append((int(number_buffer), index - len(number_buffer), index - 1))
                number_buffer = ""

    if number_buffer != "":
        candidate_list.append((int(number_buffer), len(line) - len(number_buffer), len(line) - 1))

    valid_number_list: list = []

    for candidate in candidate_list:
        start_index = candidate[1]

        if start_index > 0:
            if line[start_index - 1] not in digit_list and line[start_index - 1] != '.':
                valid_number_list.append(candidate[0])
                continue

        if (start_index + len(str(candidate[0]))) < len(line) - 1:
            if line[start_index + len(str(candidate[0]))] not in digit_list and line[start_index + len(str(candidate[0]))] != '.':
                valid_number_list.append(candidate[0])
                continue

        if prev_line is not None or next_line is not None:
            iterator_start = start_index - 1 if start_index > 0 else 0
            iterator_end = start_index + len(str(candidate[0])) if start_index + len(str(candidate[0])) < len(line) - 1 else start_index + len(str(candidate[0])) - 1
            for ch in prev_line[iterator_start:iterator_end + 1]:
                if ch not in digit_list and ch != '.':
                    valid_number_list.append(candidate[0])
                    break

    return valid_number_list, candidate_list


def get_sum_line_gear_ratio(line_numers: list[list], current_line_index: int, current_line: str) -> int:
    sum_line = 0
    for index, ch in enumerate(current_line):
        if ch == "*":
            adjacent_number_list: list[int] = []

            for number, start_index, end_index in line_numers[current_line_index]:
                if index > 0 and current_line[index - 1] in digit_list and end_index == index - 1:
                    adjacent_number_list.append(number)
                if index < len(current_line) - 1 and current_line[index + 1] in digit_list and start_index == index + 1:
                    adjacent_number_list.append(number)

            iterator_start = index - 1 if index > 0 else 0
            iterator_end = index + 1 if index < len(current_line) - 1 else index

            if current_line_index > 0:
                for number, start_index, end_index in line_numers[current_line_index - 1]:
                    if start_index <= iterator_start <= end_index or start_index <= iterator_end <= end_index:
                        adjacent_number_list.append(number)

            if current_line_index < len(line_numers) - 1:
                for number, start_index, end_index in line_numers[current_line_index + 1]:
                    if start_index <= iterator_start <= end_index or start_index <= iterator_end <= end_index:
                        adjacent_number_list.append(number)

            if len(adjacent_number_list) == 2:
                sum_line += adjacent_number_list[0] * adjacent_number_list[1]

    return sum_line


def main(lines: list[str]):
    valid_no_sum = 0
    line_numbers: list[list] = []
    for index, line in enumerate(lines):
        prev_line = lines[index - 1] if index > 0 else None
        next_line = lines[index + 1] if index < len(lines) - 1 else None
        number_list, candidate_list = get_valid_number(prev_line, line, next_line)
        line_numbers.append(candidate_list)
        for number in number_list:
            valid_no_sum += number

    print(f"{valid_no_sum=}")

    gear_sum = 0
    for index, line in enumerate(lines):
        gear_ratio = get_sum_line_gear_ratio(line_numbers, index, line)
        if gear_ratio is not None:
            gear_sum += gear_ratio

    print(f"{gear_sum=}")


if __name__ == '__main__':
    print("Demo input:")
    main(day3.demoinput1.splitlines())

    print()
    print("Game input:")
    main(day3.gameinput.splitlines())
