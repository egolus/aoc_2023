from sys import maxsize
from aocd import submit, get_data


def main():
    day = 5
    year = 2023
    data = get_data(day=day, year=year)

    test_data_a = {
            """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""": 35,
    }
    test_data_b = {
            """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""": 46,
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


def get_(x, y):
    for p in y:
        if p[0] < x < p[0] + p[2]:
            return p[1] + x-p[0]
    return x


def solve_a(data):
    sol = maxsize
    seed_soil = []
    soil_fert = []
    fert_water = []
    water_light = []
    light_temp = []
    temp_humid = []
    humid_location = []

    blocks = data.split("\n\n")

    seeds = (int(t) for t in blocks[0].split(": ")[1].split())

    for block in blocks[1:]:
        block = block.splitlines()
        for line in block[1:]:
            x, y, l = (int(t) for t in line.split())
            if block[0] == "seed-to-soil map:":
                seed_soil.append((y, x, l))
            elif block[0] == "soil-to-fertilizer map:":
                soil_fert.append((y, x, l))
            elif block[0] == "fertilizer-to-water map:":
                fert_water.append((y, x, l))
            elif block[0] == "water-to-light map:":
                water_light.append((y, x, l))
            elif block[0] == "light-to-temperature map:":
                light_temp.append((y, x, l))
            elif block[0] == "temperature-to-humidity map:":
                temp_humid.append((y, x, l))
            elif block[0] == "humidity-to-location map:":
                humid_location.append((y, x, l))

    for seed in seeds:
        soil = get_(seed, seed_soil)
        fert = get_(soil, soil_fert)
        water = get_(fert, fert_water)
        light = get_(water, water_light)
        temp = get_(light, light_temp)
        humid = get_(temp, temp_humid)
        location = get_(humid, humid_location)
        sol = min(location, sol)

    return sol


def get2(xs, ys):
    out = []
    for x in xs:
        x0, x1 = x

        # out of range
        for p in ys:
            if x1 < p[0] or x0 > (p[0] + p[2]):
                continue

            # completely in
            if p[0] <= x0 and x1 <= (p[0] + p[2]):
                out.append((p[1] + x0-p[0], p[1] + x1-p[0]))
                x1 = x0

            # lower half
            if p[0] >= x0 and x1 <= (p[0] + p[2]):
                out.append((p[1], p[1] + x1-p[0]))
                x1 = p[0]

            # upper half
            if p[0] <= x0 and x1 >= (p[0] + p[2]):
                out.append((p[1] + x0-p[0], p[1] + p[2]))
                x0 = p[0] + p[2]

        if x1 > x0:
            out.append((x0, x1))
    return out


def solve_b(data):
    sol = maxsize
    seed_soil = []
    soil_fert = []
    fert_water = []
    water_light = []
    light_temp = []
    temp_humid = []
    humid_location = []

    blocks = data.split("\n\n")

    bseed = (int(t) for t in blocks[0].split(": ")[1].split())

    for block in blocks[1:]:
        block = block.splitlines()
        for line in block[1:]:
            x, y, l = (int(t) for t in line.split())
            if block[0] == "seed-to-soil map:":
                seed_soil.append((y, x, l))
            elif block[0] == "soil-to-fertilizer map:":
                soil_fert.append((y, x, l))
            elif block[0] == "fertilizer-to-water map:":
                fert_water.append((y, x, l))
            elif block[0] == "water-to-light map:":
                water_light.append((y, x, l))
            elif block[0] == "light-to-temperature map:":
                light_temp.append((y, x, l))
            elif block[0] == "temperature-to-humidity map:":
                temp_humid.append((y, x, l))
            elif block[0] == "humidity-to-location map:":
                humid_location.append((y, x, l))

    seeds = []
    iseeds = iter(bseed)
    for seed0 in iseeds:
        seeds.append((seed0, seed0 + next(iseeds)))

    soil = get2(seeds, seed_soil)
    fert = get2(soil, soil_fert)
    water = get2(fert, fert_water)
    light = get2(water, water_light)
    temp = get2(light, light_temp)
    humid = get2(temp, temp_humid)
    location = get2(humid, humid_location)
    for l in location:
        sol = min(l[0], sol)

    return sol



if __name__ == "__main__":
    main()
