from functools import reduce


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b) if a and b else 0


def find_lcm_of_list(numbers: list[int]) -> int:
    return reduce(lcm, numbers)
