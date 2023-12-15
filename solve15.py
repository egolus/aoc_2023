from aocd import submit, get_data
from collections import defaultdict


def main():
    day = 15
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            "HASH": 52,
            "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7": 1320,
    }
    test_data_b = {
            "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7": 145,
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


class Hash():
    current = 0

    def __call__(self, s):
        for c in s:
            self.char(c)
        return self.current

    def char(self, c):
        self.current += ord(c)

        self.current *= 17
        self.current = self.current % 256


def solve_a(data):
    res = 0
    data = data.replace("\n", "")
    for p in data.strip().split(","):
        h = Hash()
        val = h(p)
        res += val
    return res


def solve_b(data):
    ans = 0
    hashmap = defaultdict(dict)
    data = data.replace("\n", "")
    for p in data.strip().split(","):
        box = Hash()(p[-1] if "-" in p else p.split("=")[0])
        if "-" in p:
            for box in hashmap:
                if p[:-1] in hashmap[box]:
                    hashmap[box].pop(p[:-1])
        elif "=" in p:
            k, v = p.split("=")
            hashmap[box][k] = v

    for k, v in sorted(hashmap.items()):
        box = k + 1
        for i, l in enumerate(v.values()):
            s = i + 1
            l = int(l)
            ans += box * s * l
    return ans


if __name__ == "__main__":
    main()
