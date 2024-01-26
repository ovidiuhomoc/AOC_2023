from collections import Counter

import day7


class Hand:
    game_cards_part_1 = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
    game_cards_part_2 = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2, 'J': 1}

    combinations = {7: 'Five of a kind',  # AAAAA
                    6: 'Four of a kind',  # AA8AA
                    5: 'Full house',  # 23332
                    4: 'Three of a kind',  # TTT98
                    3: 'Two pair',  # 23432
                    2: 'One pair',  # A23A4
                    1: 'High card'  # 23456
                    }

    def __init__(self, line: str, part: str):
        self.part = part
        self._line = line
        self.cards: list[str] = [cards for cards_str in line.split()[0] for cards in cards_str]
        self.bid: int = int(line.split()[1])
        self.power: int = self._get_power()

    def __eq__(self, other):
        c = Counter(list(self.cards))
        other_c = Counter(list(other.cards))

        for this_key in c.keys():
            if this_key not in other_c.keys():
                return False

            if c[this_key] != other_c[this_key]:
                return False

        return True

    def __gt__(self, other):
        if self.power and other.power:
            if self.power > other.power:
                return True
            elif self.power == other.power:
                for index, ch in enumerate(self.cards):
                    if self.part == "part1":
                        game_cards = self.game_cards_part_1
                    else:
                        game_cards = self.game_cards_part_2

                    if game_cards[ch] > game_cards[other.cards[index]]:
                        return True
                    elif game_cards[ch] < game_cards[other.cards[index]]:
                        return False

    def _get_power(self):
        c = Counter(self.cards)

        max_of_a_kind = max(c.values())
        if max_of_a_kind == 5:
            return 7

        elif max_of_a_kind == 4:
            return 7 if self.part2 and "J" in self.cards else 6

        elif max_of_a_kind == 3:
            if len(c) == 2:
                # 3 + 2
                return 5 if self.part1 or (self.part2 and "J" not in self.cards) else 7
            else:
                # 3 + 1 + 1
                return 4 if self.part1 or (self.part2 and "J" not in self.cards) else 6

        elif max_of_a_kind == 2:
            # 1 or 2 pairs
            if list(c.values()).count(2) == 2:
                # 2 pairs | 2 + 2 + 1
                return 3 if self.part1 or (self.part2 and "J" not in self.cards) else 5 if c["J"] == 1 else 6
            else:
                # 1 pair | 2 + 1 + 1 +1
                return 2 if self.part1 or (self.part2 and "J" not in self.cards) else 4

        else:
            return 1 if self.part1 or (self.part2 and "J" not in self.cards) else 2

    @property
    def line(self):
        return self._line

    @property
    def part1(self):
        return self.part == "part1"

    @property
    def part2(self):
        return self.part == "part2"


def main(input_str: str, part: str):
    hands_list: list[Hand] = [Hand(line, part) for line in input_str.splitlines()]
    hands_list.sort(reverse=True)

    total_winnings = sum([(len(hands_list) - index) * hand.bid for index, hand in enumerate(hands_list)])
    print(f"({part}) Total winnings: {total_winnings}")


if __name__ == '__main__':
    # main(day7.demoinput,"part1")
    # main(day7.demoinput,"part2")

    main(day7.gameinput, "part1")
    main(day7.gameinput, "part2")
