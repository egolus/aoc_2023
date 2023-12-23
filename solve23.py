from aocd import submit, get_data
import sys
from collections import defaultdict
from copy import copy
from pprint import pprint

sys.setrecursionlimit(10_000)


def main():

    day = 23
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """#.#####################
               #.......#########...###
               #######.#########.#.###
               ###.....#.>.>.###.#.###
               ###v#####.#v#.###.#.###
               ###.>...#.#.#.....#...#
               ###v###.#.#.#########.#
               ###...#.#.#.......#...#
               #####.#.#.#######.#.###
               #.....#.#.#.......#...#
               #.#####.#.#.#########v#
               #.#...#...#...###...>.#
               #.#.#v#######v###.###v#
               #...#.>.#...>.>.#.###.#
               #####v#.#.###v#.#.###.#
               #.....#...#...#.#.#...#
               #.#########.###.#.#.###
               #...###...#...#...#.###
               ###.###.#.###v#####v###
               #...#...#.#.>.>.#.>.###
               #.###.###.#.###.#.#v###
               #.....###...###...#...#
               #####################.#""": 94,
    }
    test_data_b = {
            """#.#####################
               #.......#########...###
               #######.#########.#.###
               ###.....#.>.>.###.#.###
               ###v#####.#v#.###.#.###
               ###.>...#.#.#.....#...#
               ###v###.#.#.#########.#
               ###...#.#.#.......#...#
               #####.#.#.#######.#.###
               #.....#.#.#.......#...#
               #.#####.#.#.#########v#
               #.#...#...#...###...>.#
               #.#.#v#######v###.###v#
               #...#.>.#...>.>.#.###.#
               #####v#.#.###v#.#.###.#
               #.....#...#...#.#.#...#
               #.#########.###.#.#.###
               #...###...#...#...#.###
               ###.###.#.###v#####v###
               #...#...#.#.>.>.#.>.###
               #.###.###.#.###.#.#v###
               #.....###...###...#...#
               #####################.#""": 154,
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


slopes = {
    "^": (-1, 0),
    "<": (0, -1),
    ">": (0, 1),
    "v": (1, 0)
}


def takePath(grid, pos, target, path, longest):
    finished = True
    for n in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        npos = pos[0] + n[0], pos[1] + n[1]
        if npos in grid and npos not in path:
            if grid[npos] != "." and slopes[grid[npos]] != n:
                continue
            finished = False
            longest = takePath(grid, npos, target, path+[pos], longest)
        if finished:
            if pos == target:
                longest = sorted((longest, path), key=lambda x: len(x))[-1]
    return longest


def solve_a(data):
    grid = {}
    start = None
    target = None

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != "#":
                grid[(y, x)] = c
    maxy = y
    maxx = x
    for x in range(maxx + 1):
        if (0, x) in grid:
            start = (0, x)
    for x in range(maxx + 1):
        if (maxy, x) in grid:
            target = (maxy, x)

    longest = takePath(grid, start, target, [], [])
    return len(longest)


inter = None


def flood(grid: dict, done: set, pos: tuple, target: tuple, path: list = None,
          paths: dict = None):
    if path is None:
        path = []
    if paths is None:
        paths = defaultdict(set)
    neighbours = set()
    if pos in done:
        return (done, paths)
    done.add(pos)
    for n in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        npos = pos[0] + n[0], pos[1] + n[1]
        if npos in grid and npos not in path:
            neighbours.add(npos)
    npos = next(npos for npos in neighbours)
    if len(neighbours) > 1:
        # intersection
        inter.add(pos)
        paths[tuple(sorted((path[0], pos)))].add(tuple(path))
        for npos in neighbours:
            done, paths = flood(grid, done, npos, target, [pos], paths)
    elif (
            npos in inter and
            tuple(path) not in paths[(path[0], npos)] and
            tuple(reversed(path)) not in paths[(npos, path[0])]
            ):
        # path to a known intersection
        paths[tuple(sorted((path[0], npos)))].add(tuple(path + [pos]))
    elif target in neighbours:
        # target
        paths[(path[0], target)].add(tuple(path + [pos]))
    elif not neighbours:
        # dead end
        pass
    else:
        for neighbour in neighbours:
            done, paths = flood(
                grid, done, neighbour, target, path + [pos], paths)
    return (done, paths)


def longestGraph(paths, pos, target, path=None, longest=None):
    if path is None:
        path = ([pos], 0)
    if longest is None:
        longest = ([], 0)
    for t, ps in paths.items():
        if pos in t:
            npos = next(x for x in t if x != pos)
            for p in ps:
                npath = copy(path)
                if npos not in npath[0]:
                    npath = (npath[0] + [npos], npath[1] + len(p))
                    if npos == target:
                        longest = max((longest, npath), key=lambda x: x[1])
                    else:
                        longest = longestGraph(
                            paths, npos, target, npath, longest)
    return longest


def solve_b(data):
    global inter
    inter = set()
    grid = {}
    start = None
    target = None

    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != "#":
                grid[(y, x)] = "."
    maxy = y
    maxx = x
    for x in range(maxx + 1):
        if (0, x) in grid:
            start = (0, x)
    for x in range(maxx + 1):
        if (maxy, x) in grid:
            target = (maxy, x)

    _, paths = flood(grid, set(), start, target)
    paths = dict(paths)

    longest = longestGraph(paths, start, target)

    path = []
    for t, n in list(zip(longest[0], longest[0][1:] + [longest[0][0]]))[:-1]:
        npath = paths.get((t, n), None)
        if not npath:
            npath = paths.get((n, t), None)
        npath = max(npath, key=len)
        for p in npath:
            path.append(p)

    return longest[1]


if __name__ == "__main__":
    main()
