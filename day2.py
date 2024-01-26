import day2

max_red = 12
max_green = 13
max_blue = 14


def get_game_details(string: str) -> tuple:
    # string = "1 green"
    return int(string.strip().split(" ")[0]), string.strip().split(" ")[1]


def get_game_set_details(line: str) -> tuple:
    # Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red

    game_id: int = int(line.split(":")[0].split("Game ")[1])
    game_set_details: list[tuple] = []

    for game_set in line.split(":")[1].split(";"):
        game_set_details.extend(list(map(get_game_details, game_set.split(","))))

    line_max_red = max([game[0] for game in game_set_details if game[1] == "red"])
    line_max_green = max([game[0] for game in game_set_details if game[1] == "green"])
    line_max_blue = max([game[0] for game in game_set_details if game[1] == "blue"])
    return game_id, line_max_red, line_max_green, line_max_blue


def main(multiline_input: str):
    id_sum = 0
    power_sum = 0

    for line in multiline_input.splitlines():
        game_id, line_max_red, line_max_green, line_max_blue = get_game_set_details(line)
        # print(f"For {line=}, {game_id=}, {line_max_red=}, {line_max_green=}, {line_max_blue=}")
        if line_max_red <= max_red and line_max_green <= max_green and line_max_blue <= max_blue:
            id_sum += game_id
        power_of_set = line_max_red * line_max_green * line_max_blue
        power_sum += power_of_set

    print(f"Sum of game IDs: {id_sum}")
    print(f"Sum of power: {power_sum}")


if __name__ == '__main__':
    main(day2.demoinput1)
    main(day2.gameinput)
