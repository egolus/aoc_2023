from aocd import submit, get_data
from collections import Counter


def main():
    day = 10
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """-L|F7
               7S-7|
               L|7||
               -L-J|
               L|-JF""": 4,
    }
    test_data_b = {
            """.....
            .S-7.
            .|.|.
            .L-J.
            .....""": 1,
            """...........
            .S-------7.
            .|F-----7|.
            .||.....||.
            .||.....||.
            .|L-7.F-J|.
            .|..|.|..|.
            .L--J.L--J.
            ...........""": 4,
            """.F----7F7F7F7F-7....
            .|F--7||||||||FJ....
            .||.FJ||||||||L7....
            FJL7L7LJLJ||LJ.L-7..
            L--J.L7...LJS7F-7L7.
            ....F-J..F7FJ|L7L7L7
            ....L7.F7||L7|.L7L7|
            .....|FJLJ|FJ|F7|.LJ
            ....FJL-7.||.||||...
            ....L---J.LJ.LJLJ...""": 8,
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


directions = {
    "N": (("|", "N"), ("7", "W"), ("F", "E"), ("S", None)),
    "S": (("|", "S"), ("L", "E"), ("J", "W"), ("S", None)),
    "E": (("-", "E"), ("J", "N"), ("7", "S"), ("S", None)),
    "W": (("-", "W"), ("L", "N"), ("F", "S"), ("S", None)),
}
corners = {
    "S": (("7", "W"), ("F", "E")),
    "N": (("L", "E"), ("J", "W")),
    "W": (("J", "N"), ("7", "S")),
    "E": (("L", "N"), ("F", "S")),
}
pipes = {}
pipe = set()
search = set()
check = set()
checked = set()
outside = {}


def step(old, count):
    count += 1
    if old[1] == "N":
        newPos = (old[0][0] - 1, old[0][1])
    elif old[1] == "S":
        newPos = (old[0][0] + 1, old[0][1])
    elif old[1] == "W":
        newPos = (old[0][0], old[0][1] - 1)
    elif old[1] == "E":
        newPos = (old[0][0], old[0][1] + 1)

    newDir = dict(directions[old[1]])[pipes[newPos]]
    if newDir is not None:
        return ((newPos, newDir), count)
    else:
        return (None, count)
    return count


def solve_a(data):
    """
    S - Start
    | - N-S
    - - E-W
    L - N-E
    J - N-W
    7 - S-W
    F - S-E
    . - Ground
    S - Start
    """
    pos = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != ".":
                pipes[(y, x)] = c
            if c == "S":
                pos = (y, x)

    for s in (((-1, 0), "N"), ((1, 0), "S"), ((0, -1), "W"), ((0, 1), "E")):
        n = ((pos[0] + s[0][0], pos[1] + s[0][1]), s[1])
        if ((s[1] == "N" and pipes[n[0]] not in ("|", "7", "F")) or
                (s[1] == "S" and pipes[n[0]] not in ("|", "L", "J")) or
                (s[1] == "E" and pipes[n[0]] not in ("-", "J", "7")) or
                (s[1] == "W" and pipes[n[0]] not in ("-", "L", "F"))):
            continue

        count = 1
        new = (pos, s[1])
        while new:
            new, count = step(new, count)
        return count // 2


def getCrossing(y, x):
    ps = sorted(p for p in pipe if p[0] == y and p[1] < x)
    ret = 0
    for i in range(len(ps)):
        if pipes[ps[i]] == "|":
            ret += 1
        elif pipes[ps[i]] == "L":
            for j in range(i+1, len(ps)):
                if pipes[ps[j]] == "7":
                    ret += 1
                    i += j
                    break
                if pipes[ps[j]] == "J":
                    break
        elif pipes[ps[i]] == "F":
            for j in range(i+1, len(ps)):
                if pipes[ps[j]] == "J":
                    ret += 1
                    i += j
                    break
                if pipes[ps[j]] == "7":
                    break
    return ret


def solve_b(data):
    """
    S - Start
    | - N-S
    - - E-W
    L - N-E
    J - N-W
    7 - S-W
    F - S-E
    . - Ground
    S - Start
    """
    pipes.clear()
    pipe.clear()
    search.clear()

    pos = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line.strip()):
            if c != ".":
                pipes[(y, x)] = c
            if c == "S":
                pos = (y, x)
    maxY = y
    maxX = x

    for s in (((-1, 0), "N"), ((1, 0), "S"), ((0, -1), "W"), ((0, 1), "E")):
        n = ((pos[0] + s[0][0], pos[1] + s[0][1]), s[1])
        if n[0] not in pipes:
            continue
        if ((s[1] == "N" and pipes[n[0]] not in ("|", "7", "F")) or
                (s[1] == "S" and pipes[n[0]] not in ("|", "L", "J")) or
                (s[1] == "E" and pipes[n[0]] not in ("-", "J", "7")) or
                (s[1] == "W" and pipes[n[0]] not in ("-", "L", "F"))):
            continue

        new = (pos, s[1])
        while new:
            pipe.add(new[0])
            new, _ = step(new, 0)
        break

    for y in range(maxY):
        for x in range(maxX):
            if (y, x) not in pipe:
                search.add((y, x))

    ans = 0
    for (y, x) in search:
        crossing = getCrossing(y, x)
        if crossing % 2:
            pipes[(y, x)] = "I"
            ans += 1
    return ans


if __name__ == "__main__":
    main()


