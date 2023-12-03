from aocd import submit, get_data


def main():
    day = 3
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """467..114..
            ...*......
            ..35..633.
            ......#...
            617*......
            .....+.58.
            ..592.....
            ......755.
            ...$.*....
            .664.598..""": 4361,
    }
    test_data_b = {
            """467..114..
            ...*......
            ..35..633.
            ......#...
            617*......
            .....+.58.
            ..592.....
            ......755.
            ...$.*....
            .664.598..""": 467835,
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
    sol = 0
    maxX = 0
    maxY = 0
    schematic = {}
    for i, line in enumerate(data.splitlines()):
        maxX = 0
        for j, c in enumerate(line.strip()):
            schematic[(i, j)] = c
            maxX += 1
        maxY += 1

    num = []
    for y in range(maxY):
        for x in range(maxX):
            if schematic[(y, x)].isnumeric():
                num.append((y, x))
            else:
                if num:
                    found = False
                    for yo in range(num[0][0]-1, num[0][0]+2):
                        if yo < 0 or yo >= maxY or found:
                            continue
                        for xo in range(num[0][1]-1, num[-1][1]+2):
                            if xo < 0 or xo >= maxX or found:
                                continue
                            if ((not schematic[(yo, xo)].isnumeric()) and
                                    schematic[(yo, xo)] != "." and schematic[(yo, xo)] != "x"):
                                sol += int("".join(schematic[p] for p in num))
                                for p in num:
                                    schematic[p] = "x"
                                found = True
                    num = []
        if num:
            found = False
            for yo in range(num[0][0]-1, num[0][0]+2):
                if yo < 0 or yo >= maxY or found:
                    continue
                for xo in range(num[0][1]-1, num[-1][1]+2):
                    if xo < 0 or xo >= maxX or found:
                        continue
                    if ((not schematic[(yo, xo)].isnumeric()) and
                            schematic[(yo, xo)] != "." and schematic[(yo, xo)] != "x"):
                        sol += int("".join(schematic[p] for p in num))
                        for p in num:
                            schematic[p] = "x"
                        found = True
            num = []
    return sol


def solve_b(data):
    sol = 0
    maxX = 0
    maxY = 0
    schematic = {}
    for i, line in enumerate(data.splitlines()):
        maxX = 0
        for j, c in enumerate(line.strip()):
            schematic[(i, j)] = c
            maxX += 1
        maxY += 1

    num = []
    gears = {}
    for y in range(maxY):
        for x in range(maxX):
            if schematic[(y, x)].isnumeric():
                num.append((y, x))
            else:
                if num:
                    found = False
                    for yo in range(num[0][0]-1, num[0][0]+2):
                        if yo < 0 or yo >= maxY or found:
                            continue
                        for xo in range(num[0][1]-1, num[-1][1]+2):
                            if xo < 0 or xo >= maxX or found:
                                continue
                            if schematic[(yo, xo)] == "*":
                                if (yo, xo) in gears:
                                    gears[(yo, xo)].append(num)
                                else:
                                    gears[(yo, xo)] = [num]
                                found = True
                    num = []
        if num:
            found = False
            for yo in range(num[0][0]-1, num[0][0]+2):
                if yo < 0 or yo >= maxY or found:
                    continue
                for xo in range(num[0][1]-1, num[-1][1]+2):
                    if xo < 0 or xo >= maxX or found:
                        continue
                    if schematic[(yo, xo)] == "*":
                        if (yo, xo) in gears:
                            gears[(yo, xo)].append(num)
                        else:
                            gears[(yo, xo)] = [num]
                        found = True
            num = []

    for nums in gears.values():
        if len(nums) == 2:
            sol += (int("".join(schematic[p] for p in nums[0])) *
                    int("".join(schematic[p] for p in nums[1])))

    return sol


if __name__ == "__main__":
    main()
