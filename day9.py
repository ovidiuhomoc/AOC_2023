import day9
import utils


def get_prediction(number_list: list[int]) -> tuple[int, int]:
    if all(number == 0 for number in number_list):
        # print("All zeroes")
        return 0, 0
    else:
        # print(f"Calculating for {number_list=}")
        next_level_int_list: list[int] = []
        for index, curr_number in enumerate(number_list[:-1]):
            next_level_int_list.append(number_list[index + 1] - curr_number)

        left_prediction, right_prediction = get_prediction(next_level_int_list)
        right_result = number_list[-1] + right_prediction
        left_result = number_list[0] - left_prediction

        # print(f"Returning {right_result=}")
        return left_result, right_result


def solve_challenge(input_str: str):
    sequences: list[list[int]] = list(map(utils.string_utils.to_int_list, input_str.splitlines()))

    right_seq_sum = 0
    left_seq_sum = 0
    for sequence in sequences:
        left_prediction, right_prediction = get_prediction(sequence)
        # print(f"For {sequence=} the {left_prediction=} and {right_prediction=}")
        right_seq_sum += right_prediction
        left_seq_sum += left_prediction

    print(f"Sum of predictions is{left_seq_sum=} (part 2) and  {right_seq_sum=} (part 1)")


if __name__ == '__main__':
    # solve_challenge(day9.demoinput)
    solve_challenge(day9.gameinput)
