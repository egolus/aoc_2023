from aocd import submit, get_data


def main():
    day = 18
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """R 6 (#70c710)
            D 5 (#0dc571)
            L 2 (#5713f0)
            D 2 (#d2c081)
            R 2 (#59c680)
            D 2 (#411b91)
            L 5 (#8ceee2)
            U 2 (#caa173)
            L 1 (#1b58a2)
            U 2 (#caa171)
            R 2 (#7807d2)
            U 3 (#a77fa3)
            L 2 (#015232)
            U 2 (#7a21e3)""": 62,
    }
    test_data_b = {
            """R 6 (#70c710)
            D 5 (#0dc571)
            L 2 (#5713f0)
            D 2 (#d2c081)
            R 2 (#59c680)
            D 2 (#411b91)
            L 5 (#8ceee2)
            U 2 (#caa173)
            L 1 (#1b58a2)
            U 2 (#caa171)
            R 2 (#7807d2)
            U 3 (#a77fa3)
            L 2 (#015232)
            U 2 (#7a21e3)""": 952408144115,
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
    grid = set()
    pos = [0, 0]
    for line in data.splitlines():
        line = line.strip()
        direction, length, color = line.split()
        length = int(length)
        color = color[2:-1]

        # U, D, L, R
        for i in range(length):
            if direction == "U":
                pos[0] -= 1
            elif direction == "D":
                pos[0] += 1
            elif direction == "L":
                pos[1] -= 1
            elif direction == "R":
                pos[1] += 1
            grid.add(tuple(pos))

    minY = min(k[0] for k in grid)
    maxY = max(k[0] for k in grid)
    minX = min(k[1] for k in grid)
    maxX = max(k[1] for k in grid)

    # for y in range(minY, maxY+1):
        # for x in range(minX, maxX+1):
            # print("#" if (y, x) in grid else " ", end="")
        # print()

    filler = set()
    for y in range(minY, maxY+1):
        inner = False
        top = False
        for x in range(minX, maxX+1):
            if (y, x) in grid:
                neighbours = ((-1, 0), (1, 0), (0, -1), (0, 1))
                if sum([(n[0]+y, n[1]+x) in grid for n in neighbours[:2]]):
                    # vertical wall
                    inner = not inner
                if (y, x+1) in grid and (y, x-1) not in grid:
                    # left corner
                    if (y-1, x) in grid:
                        top = True
                    else:
                        top = False
                if (y, x-1) in grid and (y, x+1) not in grid:
                    # right corner
                    if (((y+1, x) in grid and top) or
                            ((y-1, x) in grid and not top)):
                        # horizontal continuation
                        inner = not inner
            elif inner:
                filler.add((y, x))

    # for y in range(minY, maxY+1):
        # for x in range(minX, maxX+1):
            # if (y, x) in grid:
                # print("#", end="")
            # elif (y, x) in filler:
                # print(".", end="")
            # else:
                # print(" ", end="")
        # print()

    return len(grid.union(filler))


def solve_b(data):
    grid = [(0, 0)]
    pos = [0, 0]
    linearea = 0
    for line in data.splitlines():
        line = line.strip()
        color = line.split()[-1]
        color = color[2:-1]

        length = int(color[:-1], 16)
        direction = ("R", "D", "L", "U")[int(color[-1])]

        print(direction, length)

        # U, D, L, R
        if direction == "U":
            pos[0] -= length
        elif direction == "D":
            pos[0] += length
        elif direction == "L":
            pos[1] -= length
        elif direction == "R":
            pos[1] += length
        linearea += length
        grid.append(tuple(pos))

    print(grid)

    return int(area(grid) + linearea)


def intersection(grid):
    segs = segments(grid)
    for seg0, seg1 in zip(segs, segs[1:] + [segs[0]]):
        pass


def area(grid):
    return 0.5 * abs(sum(x0*y1 - x1*y0
                         for ((x0, y0), (x1, y1)) in segments(grid)))


def segments(grid):
    return zip(grid, grid[1:] + [grid[0]])


if __name__ == "__main__":
    main()
