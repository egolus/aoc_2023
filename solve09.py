from aocd import submit, get_data


def main():
    day = 9
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """0 3 6 9 12 15
            1 3 6 10 15 21
            10 13 16 21 30 45""": 114,
    }
    test_data_b = {
             """0 3 6 9 12 15
            1 3 6 10 15 21
            10 13 16 21 30 45""": 2,
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
        numbers = [[int(x) for x in line.split()]]
        while any(numbers[-1]):
            numbers.append([numbers[-1][i-1]-numbers[-1][i] for i in range(1, len(numbers[-1]))])
        for i in range(len(numbers)-2, -1, -1):
            numbers[i].append(numbers[i][-1] - numbers[i+1][-1])
        res += numbers[0][-1]
    return res


def solve_b(data):
    res = 0
    for line in data.splitlines():
        numbers = [[int(x) for x in line.split()]]
        while any(numbers[-1]):
            numbers.append([numbers[-1][i-1]-numbers[-1][i] for i in range(1, len(numbers[-1]))])
        for i in range(len(numbers)-2, -1, -1):
            numbers[i].insert(0, numbers[i][0] + numbers[i+1][0])
        res += numbers[0][0]
    return res


if __name__ == "__main__":
    main()
