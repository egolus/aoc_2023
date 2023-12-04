from aocd import submit, get_data
from collections import defaultdict


def main():
    day = 4
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11 """: 13,
    }
    test_data_b = {
            """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
            Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
            Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
            Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
            Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
            Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""": 30,
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, (test, true) in enumerate(test_data_b.items()):
        result = solve_b(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def solve_a(data):
    sol = 0

    for line in data.splitlines():
        points = 0
        line = line.strip()
        cid, other = line.split(":")
        a, b = other.split("|")
        wins = [int(x) for x in a.split()]
        mine = [int(x) for x in b.split()]
        for x in mine:
            if x in wins:
                if points == 0:
                    points = 1
                else:
                    points *= 2
        sol += points
    return sol


def solve_b(data):
    i = 0
    lines = data.splitlines()
    copies = defaultdict(int)

    for line in data.splitlines():
        points = 0
        line = line.strip()
        cid, other = line.split(":")
        a, b = other.split("|")
        wins = [int(x) for x in a.split()]
        mine = [int(x) for x in b.split()]
        for x in mine:
            if x in wins:
                points += 1
        for j in range(i+1, i+points+1):
            copies[j] += copies[i] + 1
        i += 1
    return sum(copies.values()) + len(lines)


if __name__ == "__main__":
    main()
