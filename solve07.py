from aocd import submit, get_data
from collections import defaultdict
from functools import cmp_to_key


def main():
    day = 7
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
        """32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483""": 6440,
    }
    test_data_b = {
        """32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483""": 5905,
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


cardOrder = list(reversed(["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]))
cardOrder2 = list(reversed(["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]))


def finder(hand):
    groups = defaultdict(int)
    for card in hand[0]:
        groups[card] += 1
    # groups.sort(key=lambda x: len(x))
    groups = sorted(groups.items(), key=lambda x: x[1], reverse=True)
    for i, lg in enumerate(groups):
        if lg[1] == 5:
            return 6
        elif lg[1] == 4:
            return 5
        elif lg[1] == 3:
            if 2 in (x[1] for x in groups[i+1:]):
                return 4
            return 3
        elif lg[1] == 2:
            if 2 in (x[1] for x in groups[i+1:]):
                return 2
            return 1
        return 0


def finder2(hand):
    groups = defaultdict(int)
    jokers = 0
    for card in hand[0]:
        if card == "J":
            jokers += 1
            continue
        groups[card] += 1
    groups = sorted(groups.items(), key=lambda x: x[1], reverse=True)
    if groups:
        groups[0] = (groups[0][0], groups[0][1] + jokers)
    else:
        # only jokers
        return 6
    for i, lg in enumerate(groups):
        if lg[1] == 5:
            return 6
        elif lg[1] == 4:
            return 5
        elif lg[1] == 3:
            if 2 in (x[1] for x in groups[i+1:]):
                return 4
            return 3
        elif lg[1] == 2:
            if 2 in (x[1] for x in groups[i+1:]):
                return 2
            return 1
        return 0


def cmp(x, y):
    fx = finder(x)
    fy = finder(y)
    if fx != fy:
        return -1 if fx < fy else 1
    for i in range(5):
        if x[0][i] != y[0][i]:
            return -1 if cardOrder.index(x[0][i]) < cardOrder.index(y[0][i]) else 1
    return 0


def cmp2(x, y):
    fx = finder2(x)
    fy = finder2(y)
    if fx != fy:
        return -1 if fx < fy else 1
    for i in range(5):
        if x[0][i] != y[0][i]:
            return -1 if cardOrder2.index(x[0][i]) < cardOrder2.index(y[0][i]) else 1
    return 0


def solve_a(data):
    hands = []
    for line in data.splitlines():
        hands.append(line.split())
    hands = sorted(hands, key=cmp_to_key(cmp))
    return sum(int(x[1]) * (i+1) for (i, x) in enumerate(hands))


def solve_b(data):
    hands = []
    for line in data.splitlines():
        hands.append(line.split())
    hands = sorted(hands, key=cmp_to_key(cmp2))
    return sum(int(x[1]) * (i+1) for (i, x) in enumerate(hands))


if __name__ == "__main__":
    main()
