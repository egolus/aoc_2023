from aocd import submit, get_data


def main():
    day = 6
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """Time:      7  15   30
Distance:  9  40  200""": 288,
    }
    test_data_b = {
            """Time:      7  15   30
Distance:  9  40  200""": 71503,
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
    res = 1
    tl, dl = [ln.split(":")[1] for ln in data.splitlines()]
    times = [int(x) for x in tl.split()]
    dists = [int(x) for x in dl.split()]

    for r in range(len(times)):
        time, dist = times[r], dists[r]
        forces = [(time - i) * i for i in range(time)]
        wins = [x for x in forces if x > dist]
        res *= len(wins)
    return res


def solve_b(data):
    tl, dl = [ln.split(":")[1] for ln in data.splitlines()]
    time = int(tl.replace(" ", ""))
    dist = int(dl.replace(" ", ""))
    forces = [(time - i) * i for i in range(time)]
    wins = [x for x in forces if x > dist]
    return len(wins)


if __name__ == "__main__":
    main()
