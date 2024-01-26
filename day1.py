import day1
import utils

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
string_digits = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
reversed_string_digits = []
max_string_window = 5


def get_first_digit(line, reversed_string: bool = False, include_written_numbers: bool = False) -> int:
    for index, ch in enumerate(line):
        if ch in digits:
            return int(ch)
        else:
            if not include_written_numbers:
                continue

            left_pos = index
            right_pos = index + max_string_window
            candidate_string = line[left_pos:right_pos]

            for digit_index, str_digit in enumerate(reversed_string_digits if reversed_string else string_digits):
                if str_digit[:1] != ch:
                    continue

                if str_digit in candidate_string:
                    return digit_index


def extract_number(line, include_written_numbers: bool = False) -> int:
    result = int(f"{get_first_digit(line, include_written_numbers=include_written_numbers)}{get_first_digit(utils.string_utils.get_reverse(line), reversed_string=True, include_written_numbers=include_written_numbers)}")
    # print(f"Line number for {line} is {result=}")
    return result


def part1(inputmultilinestring: str) -> int:
    all_lines_sum = 0
    for line in inputmultilinestring.splitlines():
        all_lines_sum += extract_number(line)
    # print(all_lines_sum)
    return all_lines_sum


def part2(inputmultilinestring: str) -> int:
    all_lines_sum = 0
    for line in inputmultilinestring.splitlines():
        all_lines_sum += extract_number(line, include_written_numbers=True)
    # print(all_lines_sum)
    return all_lines_sum


if __name__ == '__main__':
    for string_digit in string_digits:
        reversed_string_digits.append(utils.string_utils.get_reverse(string_digit))

    print(f"{part1(day1.demoinput1)=}")
    print(f"{part1(day1.gameinput)=}")
    print(f"{part2(day1.demoinput2)=}")
    print(f"{part2(day1.gameinput)=}")
