from aocd import submit, get_data
from collections import Counter
from copy import copy


def main():
    day = 13
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """#.##..##.
               ..#.##.#.
               ##......#
               ##......#
               ..#.##.#.
               ..##..##.
               #.#.##.#.

               #...##..#
               #....#..#
               ..##..###
               #####.##.
               #####.##.
               ..##..###
               #....#..#""": 405,
            """..##.###..###.##.
               ##..#..#..#..#..#
               ###..#..##..#.###
               ##..##########..#
               ###.####..####.##
               ..#...#.##.#...#.
               ##..#.#....#.#..#
               ..#.##.####.##.#.
               ..##.########.##.""": 1,
            """###.#.###.#.#.###
               .#.........####.#
               ...#.#####.#.####
               ###.....##.##...#
               #.######...##.#.#
               .#.#.#.......##..
               .#.#.#.......##..
               #.######...##.#.#
               ###.....##.##...#
               ...#.#####.#.####
               .#....#....####.#
               ###.#.###.#.#.###
               ###.#.###.#.#.###""": 1200,
    }
    test_data_b = {
            """#.##..##.
               ..#.##.#.
               ##......#
               ##......#
               ..#.##.#.
               ..##..##.
               #.#.##.#.

               #...##..#
               #....#..#
               ..##..###
               #####.##.
               #####.##.
               ..##..###
               #....#..#""": 400,
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
    ret = 0
    patterns = data.split("\n\n")
    for p, pattern in enumerate(patterns):
        lines = pattern.splitlines()
        cols = ["" for _ in range(len(lines[0].strip()))]
        for line in lines:
            for i, c in enumerate(line.strip()):
                cols[i] += c

        found = False

        dropped = 0
        bcols = copy(cols)
        bdropped = 0

        for i in range(len(cols) - 2):
            cols = cols[1:]
            bcols = bcols[:-1]
            dropped += 1
            bdropped += 1
            if len(cols) % 2:
                continue
            elif cols == list(reversed(cols)):
                found = True
                bdropped = 0
                break
            elif bcols == list(reversed(bcols)):
                found = True
                dropped = 0
                break

        if found:
            ret += dropped + len(cols)//2
        else:
            lines = [line.strip() for line in pattern.splitlines()]
            found = False

            dropped = 0
            blines = copy(lines)
            bdropped = 0
            for i in range(len(lines) - 2):
                lines = lines[1:]
                dropped += 1
                blines = blines[:-1]
                bdropped += 1
                if len(lines) % 2:
                    continue
                elif lines == list(reversed(lines)):
                    bdropped = 0
                    found = True
                    break
                elif blines == list(reversed(blines)):
                    dropped = 0
                    found = True
                    break
            if found:
                ret += (dropped + len(lines)//2) * 100
            else:
                print("NOT FOUND")
                print(p, pattern)
                raise Exception("NOT FOUND")
    return ret


def find(lines, ori=0):
    cols = ["" for _ in range(len(lines[0]))]
    for line in lines:
        for i, c in enumerate(line):
            cols[i] += c
    bcols = cols
    blines = lines

    if lines == list(reversed(lines)) and (len(lines)//2) * 100 != ori:
        input("middle row")
        return (dropped + len(lines)//2) * 100
    elif cols == list(reversed(cols)) and len(cols)//2 != ori:
        input("middle col")
        return dropped + len(cols)//2

    dropped = 0
    bdropped = 0
    for i in range(len(lines) - 2):
        lines = lines[1:]
        dropped += 1
        blines = blines[:-1]
        bdropped += 1
        if len(lines) % 2:
            continue
        elif lines == list(reversed(lines)) and (dropped + len(lines)//2) * 100 != ori:
            bdropped = 0
            # print(dropped, (dropped + len(lines)//2) * 100, bdropped)
            return (dropped + len(lines)//2) * 100
        elif blines == list(reversed(blines)) and len(lines)//2 * 100 != ori:
            dropped = 0
            # print(dropped, (dropped + len(lines)//2) * 100, bdropped)
            return (dropped + len(lines)//2) * 100
    dropped = 0
    bdropped = 0
    for i in range(len(cols) - 2):
        cols = cols[1:]
        bcols = bcols[:-1]
        dropped += 1
        bdropped += 1
        if len(cols) % 2:
            continue
        elif cols == list(reversed(cols)) and dropped + len(cols)//2 != ori:
            bdropped = 0
            # print(dropped, dropped + len(cols)//2, bdropped)
            return dropped + len(cols)//2
        elif bcols == list(reversed(bcols)) and len(cols)//2 != ori:
            dropped = 0
            # print(dropped, dropped + len(cols)//2, bdropped)
            return dropped + len(cols)//2


def solve_b(data):
    ret = 0
    patterns = data.split("\n\n")
    for p, pattern in enumerate(patterns):
        lines = [[c for c in line.strip()] for line in pattern.splitlines()]
        ori = find(lines)
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                tmp = [copy(line) for line in lines]
                tmp[i][j] = "#" if tmp[i][j] == "." else "."
                lr = find(tmp, ori)
                if lr and lr != ori:
                    break
            if lr and lr != ori:
                break
        if not lr or lr == ori:
            print(f"NOT FOUND {p}")
            print(pattern)
            print(f"y: {len(lines)} x: {len(lines[0])}")
            input()
            lr = 0
            # raise Exception(f"NOT FOUND {p}")
        ret += lr

        print(ret)
        print()

    return ret







if __name__ == "__main__":
    main()
