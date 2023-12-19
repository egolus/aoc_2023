from aocd import submit, get_data
from copy import copy
from pprint import pprint


def main():
    day = 19
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """px{a<2006:qkq,m>2090:A,rfg}
            pv{a>1716:R,A}
            lnx{m>1548:A,A}
            rfg{s<537:gd,x>2440:R,A}
            qs{s>3448:A,lnx}
            qkq{x<1416:A,crn}
            crn{x>2662:A,R}
            in{s<1351:px,qqz}
            qqz{s>2770:qs,m<1801:hdj,R}
            gd{a>3333:R,R}
            hdj{m>838:A,pv}

            {x=787,m=2655,a=1222,s=2876}
            {x=1679,m=44,a=2067,s=496}
            {x=2036,m=264,a=79,s=2244}
            {x=2461,m=1339,a=466,s=291}
            {x=2127,m=1623,a=2188,s=1013}""": 19114,
    }
    test_data_b = {
            """px{a<2006:qkq,m>2090:A,rfg}
            pv{a>1716:R,A}
            lnx{m>1548:A,A}
            rfg{s<537:gd,x>2440:R,A}
            qs{s>3448:A,lnx}
            qkq{x<1416:A,crn}
            crn{x>2662:A,R}
            in{s<1351:px,qqz}
            qqz{s>2770:qs,m<1801:hdj,R}
            gd{a>3333:R,R}
            hdj{m>838:A,pv}

            {x=787,m=2655,a=1222,s=2876}
            {x=1679,m=44,a=2067,s=496}
            {x=2036,m=264,a=79,s=2244}
            {x=2461,m=1339,a=466,s=291}
            {x=2127,m=1623,a=2188,s=1013}""": 167409079868000,
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
    ans = 0
    workflows = {}

    wfs, parts = data.split("\n\n")
    for line in wfs.splitlines():
        line = line.strip()
        name, rest = line.split("{")  # }
        rest = rest[:-1]
        rules = []
        for rule in rest.split(",")[:-1]:
            check, target = rule.split(":")
            if "<" in check:
                check = check.split("<")
                a, b = check
                rules.append(("<", a, int(b), target))
            else:
                assert ">" in check
                check = check.split(">")
                a, b = check
                rules.append((">", a, int(b), target))
        workflows[name] = (rules, rest.split(",")[-1])

    for line in parts.splitlines():
        line = line.strip()[1:-1]
        vals = {}
        for p in line.split(","):
            k, v = p.split("=")
            vals[k] = int(v)
        pos = "in"
        while pos:
            rules, target = workflows[pos]
            for i, rule in enumerate(rules):
                if ((rule[0] == "<" and vals[rule[1]] < rule[2]) or
                        (rule[0] == ">" and vals[rule[1]] > rule[2])):
                    pos = rule[3]
                    break
            else:
                pos = target
            if pos == "A":
                ans += sum(vals.values())
                break
            elif pos == "R":
                break
    return ans


def getlimits(limits, workflows, pos):
    print(f"getlimits {limits=} {pos=}")
    found = False
    if pos == "A":
        return limits
    elif pos == "R":
        return
    rules, target = workflows[pos]
    tl = getlimits(limits, workflows, target)
    if tl:
        found = True
        for p in ("x", "m", "a", "s"):
            limits[p] = (
                max(limits[p][0], tl[p][0]),
                min(limits[p][1], tl[p][1])
            )
    for rule in rules:
        nl = {
            "x": copy(limits["x"]),
            "m": copy(limits["m"]),
            "a": copy(limits["a"]),
            "s": copy(limits["s"]),
        }
        if rule[0] == "<":
            pass
        else:
            assert rule[0] == ">"
            pass

        tl = getlimits(limits, workflows, rule[3])
        if tl:
            found = True
            for p in ("x", "m", "a", "s"):
                limits[p] = (
                    max(limits[p][0], tl[p][0]),
                    min(limits[p][1], tl[p][1])
                )
    if found:
        return limits


def solve_b(data):
    ans = 0
    workflows = {}

    wfs = data.split("\n\n")[0]
    for line in wfs.splitlines():
        line = line.strip()
        name, rest = line.split("{")  # }
        rest = rest[:-1]
        rules = []
        for rule in rest.split(",")[:-1]:
            check, target = rule.split(":")
            if "<" in check:
                check = check.split("<")
                a, b = check
                rules.append(("<", a, int(b), target))
            else:
                assert ">" in check
                check = check.split(">")
                a, b = check
                rules.append((">", a, int(b), target))
        workflows[name] = (rules, rest.split(",")[-1])

    pos = "in"
    ranges = {"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}
    print(getlimits(ranges, workflows, "in"))

    # while pos:
        # rules, target = workflows[pos]
        # limits = {"x": [4000, 1], "m": [4000, 1], "a": [4000, 1], "s": [4000, 1]}
        # for rule in rules:
            # if rule[0] == ">":
                # limits[rule[1]] = max(limits[rule[1]][1], rule[2])
            # else:
                # assert rule[0] == "<", rule[0]
                # limits[rule[1]] = min(limits[rule[1]][0], rule[2])
        # print(limits)


if __name__ == "__main__":
    main()
