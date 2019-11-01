import argparse
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Tuple
from functools import reduce


class Direction(Enum):
    North = auto()
    East = auto()
    South = auto()
    West = auto()


class Command(Enum):
    Left = auto()
    Right = auto()
    Forward = auto()


@dataclass()
class Position:
    x: int
    y: int

    def as_tuple(self):
        return self.x, self.y


@dataclass()
class Robot:
    position: Position
    direction: Direction


@dataclass()
class Journey:
    start: Robot
    end: Robot
    commands: List[Command]


direction_map = {
    "N": Direction.North,
    "E": Direction.East,
    "S": Direction.South,
    "W": Direction.West,
}


command_map = {
    "L": Command.Left,
    "R": Command.Right,
    "F": Command.Forward,
}


def parse_robot(line: str) -> Robot:
    parts = line.split()
    x = int(parts[0])
    y = int(parts[1])
    direction = direction_map[parts[2]]

    return Robot(position=Position(x=x, y=y), direction=direction)


def handle_command(robot: Robot, command: Command):
    # possibly treating auto enums as ints is a bit too magic, depending on taste a more explicit mapping might be preferred
    if command == Command.Left:
        val = robot.direction.value - 1
        new_direction = (
            Direction.West if val < Direction.North.value else Direction(val)
        )
        new_position = robot.position

    elif command == Command.Right:
        val = robot.direction.value + 1
        new_direction = (
            Direction.North if val > Direction.West.value else Direction(val)
        )
        new_position = robot.position

    else:  # command == Command.Forward:
        new_direction = robot.direction
        x = robot.position.x
        y = robot.position.y
        if robot.direction == Direction.North:
            new_position = Position(x=x, y=y + 1)
        elif robot.direction == Direction.East:
            new_position = Position(x=x + 1, y=y)
        elif robot.direction == Direction.South:
            new_position = Position(x=x, y=y - 1)
        else:  # robot.direction == Direction.West:
            new_position = Position(x=x - 1, y=y)

    return Robot(new_position, new_direction)


def is_journey_valid(lines: List[str]) -> Tuple[bool, Robot]:
    start = parse_robot(lines[0])
    commands = [command_map[c] for c in lines[1]]
    proposed_end = parse_robot(lines[2])

    # possibly reduce() is unpythonic, depending on taste a standard for loop might be preferred
    actual_end = reduce(handle_command, commands, start)

    return (
        proposed_end.direction == actual_end.direction
        and proposed_end.position.as_tuple() == actual_end.position.as_tuple()
    ), actual_end


def main():
    parser = argparse.ArgumentParser(description="Process robot journeys.")
    parser.add_argument("file_path", help="path to input file")

    args = parser.parse_args()

    with open(args.file_path, "r") as f:
        result = is_journey_valid(f.readlines())
    print(result)


if __name__ == "__main__":
    main()
