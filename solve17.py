from aocd import submit, get_data
import sys


def main():
    day = 17
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """2413432311323
            3215453535623
            3255245654254
            3446585845452
            4546657867536
            1438598798454
            4457876987766
            3637877979653
            4654967986887
            4564679986453
            1224686865563
            2546548887735
            4322674655533""": 102,
    }
    test_data_b = {
            """2413432311323
            3215453535623
            3255245654254
            3446585845452
            4546657867536
            1438598798454
            4457876987766
            3637877979653
            4654967986887
            4564679986453
            1224686865563
            2546548887735
            4322674655533""": 94,
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


def getNeighbors(current, minStraight, maxStraight):
    """
    current = (y, x, direction, steps)
    """
    neighbors = []
    dirs = [-1, 0, 1]
    if -1 < current[3] < minStraight:
        dirs = [0]
    if current[3] >= maxStraight:
        dirs.remove(0)
    for dir in dirs:
        if current[2] == "n":
            if dir == -1:
                neighbors.append((current[0], current[1]-1, "w", 0))
            elif dir == 0:
                neighbors.append((current[0]-1, current[1], "n", current[3]+1))
            elif dir == 1:
                neighbors.append((current[0], current[1]+1, "e", 0))
        elif current[2] == "s":
            if dir == -1:
                neighbors.append((current[0], current[1]+1, "e", 0))
            elif dir == 0:
                neighbors.append((current[0]+1, current[1], "s", current[3]+1))
            elif dir == 1:
                neighbors.append((current[0], current[1]-1, "w", 0))
        elif current[2] == "e":
            if dir == -1:
                neighbors.append((current[0]-1, current[1], "n", 0))
            elif dir == 0:
                neighbors.append((current[0], current[1]+1, "e", current[3]+1))
            elif dir == 1:
                neighbors.append((current[0]+1, current[1], "s", 0))
        elif current[2] == "w":
            if dir == -1:
                neighbors.append((current[0]+1, current[1], "s", 0))
            elif dir == 0:
                neighbors.append((current[0], current[1]-1, "w", current[3]+1))
            elif dir == 1:
                neighbors.append((current[0]-1, current[1], "n", 0))
    return neighbors


def astar(grid, position, target, h, minStraight, maxStraight):
    """
    a* from position to target

    neighbor = (y, x, direction, steps)
    """
    start = position
    openSet = {start}
    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = h(start)

    while openSet:
        current = min(openSet, key=lambda a: fScore.get(a, sys.maxsize))
        if current[:2] == target:
            break
        openSet.remove(current)
        neighbors = getNeighbors(current, minStraight, maxStraight)
        for neighbor in sorted(neighbors, key=lambda x: grid.get(x[:2], sys.maxsize)):
            if neighbor[:2] not in grid:
                continue
            tentativeGScore = gScore[current] + grid[neighbor[:2]]
            if (neighbor not in gScore) or (tentativeGScore < gScore[neighbor]):
                cameFrom[neighbor] = current
                gScore[neighbor] = tentativeGScore
                fScore[neighbor] = tentativeGScore + h(neighbor)
                openSet.add(neighbor)

    # pprint(cameFrom)
    if current[:2] == target:
        path = [current[:2]]
        while current in cameFrom.keys():
            current = cameFrom[current]
            path = [current[:2]] + path
        path.pop(0)
        return path


def havg(start, target, avg):
    return (abs(start[0] - target[0]) + abs(start[1] - target[1]))


def solve_a(data):
    grid = {}
    s = 0  # sum of all values
    avg = 0  # avg of all values
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y, x)] = int(c)
            s += int(c)
    maxY = y
    maxX = x
    avg = s // (maxY * maxX)

    for y in range(maxY+1):
        for x in range(maxX+1):
            print(grid[(y, x)], end="")
        print()

    start = (0, 0, "e", -1)
    target = (maxY, maxX)
    path = astar(grid, start, target, lambda x: havg(x, target, avg), minStraight=0, maxStraight=2)

    for y in range(maxY+1):
        for x in range(maxX+1):
            if (y, x) in path:
                print("x", end="")
            else:
                print(".", end="")
        print()
    return sum(grid[x] for x in path)


def solve_b(data):
    grid = {}
    s = 0  # sum of all values
    avg = 0  # avg of all values
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            grid[(y, x)] = int(c)
            s += int(c)
    maxY = y
    maxX = x
    avg = s // (maxY * maxX)

    for y in range(maxY+1):
        for x in range(maxX+1):
            print(grid[(y, x)], end="")
        print()

    start = (0, 0, "e", -1)
    target = (maxY, maxX)
    path = astar(grid, start, target, lambda x: havg(x, target, avg), minStraight=3, maxStraight=9)

    for y in range(maxY+1):
        for x in range(maxX+1):
            if (y, x) in path:
                print("x", end="")
            else:
                # print(grid[(y, x)], end="")
                print(".", end="")
        print()
    return sum(grid[x] for x in path)


if __name__ == "__main__":
    main()
