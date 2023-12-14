from aocd import submit, get_data


def main():
    day = 14
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....""": 136,
    }
    test_data_b = {
            """O....#....
            O.OO#....#
            .....##...
            OO.#O....O
            .O.....O#.
            O.#..O.#.#
            ..O..#O..O
            .......O..
            #....###..
            #OO..#....""": 64,
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


def printGrid(grid, maxY, maxX):
    print("-"*maxX)
    for y in range(maxY):
        for x in range(maxX):
            if (y, x) in grid:
                print(grid[(y, x)], end="")
            else:
                print(" ", end="")
        print()
    print()


def solve_a(data):
    ans = 0
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c in "O#":
                grid[(y, x)] = c
    maxY = y + 1
    maxX = x + 1

    # printGrid(grid, maxY, maxX)

    for y in range(maxY):
        for x in range(maxX):
            if grid.get((y, x), "") == "O":
                dy = y
                for dy in range(y-1, -2, -1):
                    if (dy, x) in grid:
                        break
                grid[(dy+1, x)] = grid.pop((y, x))
    # printGrid(grid, maxY, maxX)

    for y in range(maxY):
        for x in range(maxX):
            if grid.get((y, x), "") == "O":
                ans += maxY - y
    return ans


def solve_b(data, cycles=1_000_000_000):
    ans = 0
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c in "O#":
                grid[(y, x)] = c
    maxY = y + 1
    maxX = x + 1

    answers = []
    for i in range(1000):
        # north
        for y in range(maxY):
            for x in range(maxX):
                if grid.get((y, x), "") == "O":
                    dy = y
                    for dy in range(y-1, -2, -1):
                        if (dy, x) in grid:
                            break
                    grid[(dy+1, x)] = grid.pop((y, x))
        # printGrid(grid, maxY, maxX)

        # west
        for x in range(maxX):
            for y in range(maxY):
                if grid.get((y, x), "") == "O":
                    dx = x
                    for dx in range(x-1, -2, -1):
                        if (y, dx) in grid:
                            break
                    grid[(y, dx+1)] = grid.pop((y, x))
        # printGrid(grid, maxY, maxX)

        # south
        for y in range(maxY, -1, -1):
            for x in range(maxX):
                if grid.get((y, x), "") == "O":
                    dy = y
                    for dy in range(y+1, maxY+1):
                        if (dy, x) in grid:
                            break
                    grid[(dy-1, x)] = grid.pop((y, x))
        # printGrid(grid, maxY, maxX)

        # east
        for x in range(maxX, -1, -1):
            for y in range(maxY):
                if grid.get((y, x), "") == "O":
                    dx = x
                    for dx in range(x+1, maxX+1):
                        if (y, dx) in grid:
                            break
                    grid[(y, dx-1)] = grid.pop((y, x))
        # printGrid(grid, maxY, maxX)

        ans = 0
        for y in range(maxY):
            for x in range(maxX):
                if grid.get((y, x), "") == "O":
                    ans += maxY - y
        answers.append(ans)
    for di in range(len(answers)-2, 0, -1):
        if (answers[di] == answers[-1] and
                answers[di-1] == answers[-2] and
                answers[di-2] == answers[-3]):
            cycleStop = di
            break
    rest = (cycles - i) % (i-cycleStop)
    return answers[cycleStop + rest - 1]


if __name__ == "__main__":
    main()
