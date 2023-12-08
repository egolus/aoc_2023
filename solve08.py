from aocd import submit, get_data


def main():
    day = 8
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """RL

            AAA = (BBB, CCC)
            BBB = (DDD, EEE)
            CCC = (ZZZ, GGG)
            DDD = (DDD, DDD)
            EEE = (EEE, EEE)
            GGG = (GGG, GGG)
            ZZZ = (ZZZ, ZZZ)""": 2,
            """LLR

            AAA = (BBB, BBB)
            BBB = (AAA, ZZZ)
            ZZZ = (ZZZ, ZZZ)""": 6,
    }
    test_data_b = {
            """LR

            11A = (11B, XXX)
            11B = (XXX, 11Z)
            11Z = (11B, XXX)
            22A = (22B, XXX)
            22B = (22C, 22C)
            22C = (22Z, 22Z)
            22Z = (22B, 22B)
            XXX = (XXX, XXX)""": 6,
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
    instructions = {}
    lines = data.splitlines()
    path = lines[0]
    for line in lines[2:]:
        a, rest = line.strip().split(" = ")
        b, c = rest.split(", ")

        instructions[a] = (b[1:], c[:-1])

    pos = "AAA"
    sol = 0
    while pos != "ZZZ":
        for step in path:
            sol += 1
            pos = instructions[pos][0] if step == "L" else instructions[pos][1]
            if pos == "ZZZ":
                break
    return sol


def primes2(n):
    sieve = [True] * (n//2)
    for i in range(3, int(n**0.5) + 1, 2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [[2, 0]] + [[2*i+1, 0] for i in range(1, n//2) if sieve[i]]


def kgv(numbers):
    result = 1
    primes = primes2(max(numbers)+1)

    for i in range(0, len(numbers)):
        for j in range(0, len([p[0] for p in primes if p[0] < numbers[i]+1])):
            c = 0
            while numbers[i] % primes[j][0] == 0:
                c += 1
                numbers[i] /= primes[j][0]
            if c > primes[j][1]:
                primes[j][1] = c
    for i in [r[0] ** r[1] for r in primes if r[1] > 0]:
        result *= i

    return result


def solve_b(data):
    instructions = {}
    positions = []
    lines = data.splitlines()
    path = lines[0]
    for line in lines[2:]:
        a, rest = line.strip().split(" = ")
        b, c = rest.split(", ")

        instructions[a] = (b[1:], c[:-1])
        if a[-1] == "Z":
            positions.append(a)

    sol = []
    now = 0
    while positions:
        for step in path:
            now += 1
            for i, pos in enumerate(positions):
                pos = instructions[pos][0] if step == "L" else instructions[pos][1]
                positions[i] = pos
            for i, pos in enumerate(positions):
                if pos[-1] == "Z":
                    sol.append(now)
                    positions.pop(i)
    return kgv(sol)


if __name__ == "__main__":
    main()
