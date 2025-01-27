from common import parse_args_and_get_input
from dataclasses import dataclass
import re
from typing import List, Tuple, Iterable
from functools import lru_cache


@dataclass(frozen=True, eq=True)
class Moon:
    x: int
    y: int
    z: int
    vel_x: int
    vel_y: int
    vel_z: int

    @classmethod
    def make(cls, coords, vels):
        return Moon(coords[0], coords[1], coords[2], vels[0], vels[1], vels[2])

    def get_coords(self):
        return [self.x, self.y, self.z]

    def get_vels(self):
        return [self.vel_x, self.vel_y, self.vel_z]


def parse_moons(lines):
    reg = "x=|y=|z=|<|>"
    moons = [re.sub(reg, "", l).split(",") for l in lines]
    moons = [[int(point) for point in moon] for moon in moons]
    return [Moon.make(coords, (0, 0, 0)) for coords in moons]


def parse_test(data: str):
    return parse_moons(data.strip().splitlines())


def do_gravity(moons: List[Moon]):
    new_moons = []

    for i, moon1 in enumerate(moons):
        moon1_coords = moon1.get_coords()
        moon1_vels = moon1.get_vels()

        for j in range(len(moons)):
            if i == j:
                continue

            moon2_coords = moons[j].get_coords()

            for coord_index, other_coord in enumerate(moon2_coords):
                if moon1_coords[coord_index] < other_coord:
                    moon1_vels[coord_index] += 1
                elif moon1_coords[coord_index] > other_coord:
                    moon1_vels[coord_index] -= 1

        new_moons.append(Moon.make(moon1_coords, moon1_vels))

    return new_moons


def do_velocity(moons: Iterable[Moon]):
    new_moons = []
    for moon in moons:
        coords = moon.get_coords()
        vels = moon.get_vels()

        new_coords = [(coord + vel) for coord, vel in zip(coords, vels)]
        new_moons.append(Moon.make(new_coords, moon.get_vels()))

    return new_moons


def calc_energy(moons: List[Moon]):
    def energy_for_moon(moon: Moon):
        return sum(abs(x) for x in moon.get_coords()) * sum(abs(x) for x in moon.get_vels())

    return sum(energy_for_moon(moon) for moon in moons)


@lru_cache(maxsize=None)
def simulate_step(moons: List[Moon]):
    moons = do_gravity(moons)
    moons = do_velocity(moons)

    return moons


def part_one(moons: List[Moon], steps: int):
    for i in range(steps):
        moons = do_gravity(moons)
        moons = do_velocity(moons)
        print(f"step {i + 1}")
        print(moons)
        print("")

    energy = calc_energy(moons)
    print(energy)


def part_two(moons: List[Moon]):
    while True:
        moons = do_gravity(moons)
        moons = do_velocity(moons)


test1 = """
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""

args, lines = parse_args_and_get_input()

if args.part_one:
    #moons = parse_moons(lines)
    #moons = parse_test(test1)
    #part_one(moons, 10)
    moons = parse_moons(lines)
    part_one(moons, 1000)
else:
    pass
