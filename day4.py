import day4
import utils

cards_queue = []
successful_numbers_list = []


def extract_card_details(line: str) -> tuple:
    all_numbers_string = line.split(': ')[1].strip()
    win_numbers: list[int] = utils.string_utils.to_int_list(all_numbers_string.split("|")[0])
    card_numbers: list[int] = utils.string_utils.to_int_list(all_numbers_string.split("|")[1])

    return win_numbers, card_numbers


def get_successful_numbers(card) -> int:
    win_numbers, card_numbers = card
    successful_numbers = sum([1 if number in card_numbers else 0 for number in win_numbers])
    return successful_numbers


def get_card_points(card: tuple) -> int:
    successful_numbers = get_successful_numbers(card)
    return 2 ** (successful_numbers - 1) if successful_numbers else 0


def part1(input_string: str):
    card_list: list[tuple] = list(map(extract_card_details, input_string.splitlines()))
    cards_worth: list[int] = list(map(get_card_points, card_list))

    print(f"All cards worth {sum(cards_worth)} points.")


def process_card(index: int):
    cards_queue.append(index)
    success_no = successful_numbers_list[index]
    if success_no:
        for i in range(index + 1, index + 1 + success_no):
            process_card(i)


def part2(input_string: str):
    card_list: list[tuple] = list(map(extract_card_details, input_string.splitlines()))
    successful_numbers_list.extend(list(map(get_successful_numbers, card_list)))

    for index, card in enumerate(card_list):
        process_card(index)

    print(f"Cards queue length: {len(cards_queue)}")


def main():
    part1(day4.demoinput)
    part2(day4.demoinput)

    part1(day4.gameinput)
    part2(day4.gameinput)


if __name__ == '__main__':
    main()
