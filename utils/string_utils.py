def get_reverse(string):
    return string[::-1]


def to_int_list(string: str) -> list[int]:
    try:
        return list(map(int, string.strip().split()))
    except ValueError as err:
        print(f"ValueError occurred while parsing {string=}.")
        raise ValueError from err
