from aocd import submit, get_data


def main():
    day = 1
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
        """1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet""": 142,
    }
    test_data_b = {
        """two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen""": 281,
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
    res = 0
    for line in data.splitlines():
        a = 0
        b = 0
        for i in line:
            if i in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                a = i
                break
        for i in reversed(line):
            if i in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
                b = i
                break
        res += int("".join((a, b)))
    return res


def solve_b(data):
    res = 0
    for line in data.splitlines():
        out = []
        digits = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8":
                  8, "9": 9, "one": 1, "two": 2, "three": 3, "four": 4, "five":
                  5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
        for digit in digits:
            linex = line
            while linex:
                if digit in linex:
                    out.append((linex.find(digit) + len(line) - len(linex), digits[digit]))
                    linex = linex[linex.find(digit)+1:]
                else:
                    break
        out = sorted(out)
        res += int("".join((str(out[0][1]), str(out[-1][1]))))
    return res


if __name__ == "__main__":
    main()
