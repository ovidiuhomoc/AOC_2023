from functools import cache

import day8
from utils.math_utils import find_lcm_of_list

nodes_dict: dict = {}


def part_1(input_string: str):
    instructions = initialize_nodes_dict(input_string)

    step_count = 0
    node = 'AAA'
    target_node = 'ZZZ'
    found = False

    for instruction in instructions_generator(instructions):
        if node == target_node:
            print(f'(Part1)  Node {node} reached in {step_count} steps.')
            found = True
            break
        else:
            node = nodes_dict[node][0] if instruction == 'L' else nodes_dict[node][1]
        step_count += 1

    if not found:
        print(f'(Part1)  Node {target_node} not reached in {step_count} steps.')


def instructions_generator(instr_str: str) -> str:
    index = 0
    while True:
        yield instr_str[index]
        index = (index + 1) % len(instr_str)


def initialize_nodes_dict(input_string) -> str:
    instructions_str, network_str = input_string.split('\n\n')
    nodes_dict.clear()
    for line in network_str.splitlines():
        node_name: str = line.split('=')[0].strip()
        node_left: str = line.split('=')[1].strip()[1:4]
        node_right: str = line.split(',')[1].strip()[:3]
        nodes_dict[node_name] = (node_left, node_right)
    return instructions_str


@cache
def get_next_node_list(nodes_list: list[str], instruction: str) -> list[str]:
    return [nodes_dict[node][0] if instruction == 'L' else nodes_dict[node][1] for node in nodes_list]


def part_2(input_string: str):
    instructions = initialize_nodes_dict(input_string)

    a_ended_nodes_list: list[str] = [node for node in nodes_dict.keys() if node.endswith('A')]
    found = False
    nodes_steps_count: list[int] = []

    for a_ended_node in a_ended_nodes_list:
        node = a_ended_node
        step_count = 0

        for instruction in instructions_generator(instructions):
            if node.endswith("Z"):
                print(f'(Part2) Node {node} end with Z and finished in {step_count} steps.')
                found = True
                nodes_steps_count.append(step_count)
                break
            node = nodes_dict[node][0] if instruction == 'L' else nodes_dict[node][1]
            step_count += 1

        if not found:
            print(f'(Part2) Node {node} - Solution not reached in {step_count} steps.')

    print(f"(Part2) LCM for {nodes_steps_count} is {find_lcm_of_list(nodes_steps_count)}")


if __name__ == '__main__':
    part_1(day8.demo_input_1)
    print()
    part_1(day8.demo_input_2)
    print()
    part_1(day8.game_input)
    print()

    part_2(day8.demo_input_3)
    print()
    part_2(day8.game_input)
