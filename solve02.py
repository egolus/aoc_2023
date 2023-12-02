from functools import reduce
from operator import mul
from aocd import submit, get_data


def main():
    day = 2
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
            Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
            Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
            Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""": 8,
    }
    test_data_b = {
            """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
            Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
            Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
            Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
            Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""": 2286,
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
    possible = []
    for line in data.splitlines():
        line = line.strip()
        cubes = {}
        game, plays = line.split(":")
        game = game.split(" ")[1]
        for x in plays.split(";"):
            for p in x.split(","):
                p = p.strip().split(" ")
                if p[1] in cubes:
                    if int(p[0]) > cubes[p[1]]:
                        cubes[p[1]] = int(p[0])
                else:
                    cubes[p[1]] = int(p[0])
        if (("red" in cubes and cubes["red"] > 12) or
                ("green" in cubes and cubes["green"] > 13) or
                ("blue" in cubes and cubes["blue"] > 14)):
            continue
        else:
            possible.append(int(game))
    return sum(possible)


def solve_b(data):
    possible = []
    for line in data.splitlines():
        line = line.strip()
        cubes = {}
        game, plays = line.split(":")
        game = game.split(" ")[1]
        for x in plays.split(";"):
            for p in x.split(","):
                p = p.strip().split(" ")
                if p[1] in cubes:
                    if int(p[0]) > cubes[p[1]]:
                        cubes[p[1]] = int(p[0])
                else:
                    cubes[p[1]] = int(p[0])
        possible.append(reduce(mul, cubes.values(), 1))
    return sum(possible)


if __name__ == "__main__":
    main()
