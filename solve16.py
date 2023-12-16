from aocd import submit, get_data
from collections import defaultdict
import sys

sys.setrecursionlimit(1_000_000_000)


def main():
    day = 16
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """.|...\\....
            |.-.\\.....
            .....|-...
            ........|.
            ..........
            .........\\
            ..../.\\\\..
            .-.-/..|..
            .|....-|.\\
            ..//.|....""": 46,
    }
    test_data_b = {
            """.|...\\....
            |.-.\\.....
            .....|-...
            ........|.
            ..........
            .........\\
            ..../.\\\\..
            .-.-/..|..
            .|....-|.\\
            ..//.|....""": 51,
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


energized = defaultdict(list)


def ntile(tile, direction):
    if direction == "n":
        tile = (tile[0]-1, tile[1])
    elif direction == "s":
        tile = (tile[0]+1, tile[1])
    elif direction == "e":
        tile = (tile[0], tile[1]+1)
    elif direction == "w":
        tile = (tile[0], tile[1]-1)
    return tile


def beam(grid, tile, direction, maxY, maxX):
    if tile[0] < 0 or tile[0] >= maxY:
        return
    if tile[1] < 0 or tile[1] >= maxX:
        return
    if direction in energized[tile]:
        return

    energized[tile].append(direction)

    if grid[tile] == ".":
        beam(grid, ntile(tile, direction), direction, maxY, maxX)
    elif grid[tile] == "/":
        if direction == "n":
            direction = "e"
        elif direction == "s":
            direction = "w"
        elif direction == "e":
            direction = "n"
        elif direction == "w":
            direction = "s"
        beam(grid, ntile(tile, direction), direction, maxY, maxX)
    elif grid[tile] == "\\":
        if direction == "n":
            direction = "w"
        elif direction == "s":
            direction = "e"
        elif direction == "e":
            direction = "s"
        elif direction == "w":
            direction = "n"
        beam(grid, ntile(tile, direction), direction, maxY, maxX)
    elif grid[tile] == "|":
        if direction == "n":
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
        elif direction == "s":
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
        elif direction == "e":
            direction = "s"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
            direction = "n"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
        elif direction == "w":
            direction = "n"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
            direction = "s"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
    elif grid[tile] == "-":
        if direction == "n":
            direction = "e"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
            direction = "w"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
        elif direction == "s":
            direction = "e"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
            direction = "w"
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
        elif direction == "e":
            beam(grid, ntile(tile, direction), direction, maxY, maxX)
        elif direction == "w":
            beam(grid, ntile(tile, direction), direction, maxY, maxX)


def solve_a(data):
    global energized
    energized = defaultdict(list)
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y, x)] = c
    maxY = y + 1
    maxX = x + 1

    beam(grid, (0, 0), "e", maxY, maxX)
    return len(energized)


def solve_b(data):
    global energized
    energized = defaultdict(list)
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y, x)] = c
    maxY = y + 1
    maxX = x + 1

    ans = 0
    for y in range(maxY):
        energized = defaultdict(list)
        beam(grid, (y, 0), "e", maxY, maxX)
        ans = max(ans, len(energized))

        energized = defaultdict(list)
        beam(grid, (y, maxX-1), "w", maxY, maxX)
        ans = max(ans, len(energized))
    for x in range(maxX):
        energized = defaultdict(list)
        beam(grid, (0, x), "s", maxY, maxX)
        ans = max(ans, len(energized))

        energized = defaultdict(list)
        beam(grid, (maxY-1, x), "n", maxY, maxX)
        ans = max(ans, len(energized))
    return ans


if __name__ == "__main__":
    main()
