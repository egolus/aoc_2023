from aocd import submit, get_data


def main():
    day = 11
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """...#......
            .......#..
            #.........
            ..........
            ......#...
            .#........
            .........#
            ..........
            .......#..
            #...#.....""": 374,
    }
    test_data_b = {
            ("""...#......
            .......#..
            #.........
            ..........
            ......#...
            .#........
            .........#
            ..........
            .......#..
            #...#.....""", 10): 1030,
            ("""...#......
            .......#..
            #.........
            ..........
            ......#...
            .#........
            .........#
            ..........
            .......#..
            #...#.....""", 100): 8410
    }

    for i, (test, true) in enumerate(test_data_a.items()):
        result = solve_a(test)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_a = solve_a(data)
    print(f"result a: {result_a}\n")
    submit(result_a, part="a", day=day, year=year)

    for i, ((test, expand), true) in enumerate(test_data_b.items()):
        result = solve_b(test, expand)
        print(f"result {i}: {result}\n")
        assert result == true, f"{result} != {true}"

    result_b = solve_b(data)
    print(f"result b: {result_b}\n")
    submit(result_b, part="b", day=day, year=year)


def solve_a(data):
    space = []
    maxX = 0
    addY = 0
    addX = []

    for y, line in enumerate(data.splitlines()):
        if all(c == "." for c in line.strip()):
            addY += 1
        for x, c in enumerate(line.strip()):
            if c == "#":
                space.append((y + addY, x))
        maxX = x

    xs = [x for (_, x) in space]
    for x in range(maxX):
        if not any(dx == x for dx in xs):
            addX.append(x)
    for i in range(len(space)):
        y, x = space[i]
        for j in range(len(addX)):
            if x > addX[j]:
                space[i] = (y, x+j+1)

    dists = []
    for i, g in enumerate(space):
        for j, h in enumerate(space[i+1:]):
            y = abs(g[0] - h[0])
            x = abs(g[1] - h[1])
            dists.append(y+x)

    return sum(dists)


def solve_b(data, expand=1_000_000):
    space = []
    maxX = 0
    addY = 0
    addX = []

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c == "#":
                space.append((y, x))
    print(space)
    space.clear()

    for y, line in enumerate(data.splitlines()):
        if all(c == "." for c in line.strip()):
            addY += (expand - 1)
        for x, c in enumerate(line.strip()):
            if c == "#":
                space.append((y + addY, x))
        maxX = x

    xs = [x for (_, x) in space]
    for x in range(maxX):
        if not any(dx == x for dx in xs):
            addX.append(x)
    print(f"addX: {addX}")
    for i in range(len(space)):
        y, x = space[i]
        for j in range(len(addX)):
            if x > addX[j]:
                space[i] = (y, x + (1 + j) * (expand - 1))

    print(space)
    dists = []
    for i, g in enumerate(space):
        for j, h in enumerate(space[i+1:]):
            y = abs(g[0] - h[0])
            x = abs(g[1] - h[1])
            print((i, j+i+1), (x, y), x+y)
            dists.append(y+x)
    print(dists)

    return sum(dists)


if __name__ == "__main__":
    main()
