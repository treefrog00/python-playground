from common import parse_args_and_get_input
from dataclasses import dataclass
from intcode import parse_program, IntComputer
from enum import Enum, auto


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Direction(Enum):
    North = auto()
    East = auto()
    South = auto()
    West = auto()


class Robot:
    def __init__(self):
        self.white_panels = set()
        self.been_painted = set()
        self.current_pos = Point(0, 0)
        self.next_ins_is_direction = False
        self.direction = Direction.North

    def get_current_color(self):
        return self.current_pos in self.white_panels

    def receive_instruction(self, ins):
        if self.next_ins_is_direction:
            new_val = self.direction.value
            if ins:
                new_val += 1
            else:
                new_val -= 1

            if new_val < Direction.North.value:
                new_val = Direction.West.value
            elif new_val > Direction.West.value:
                new_val = Direction.North.value

            self.direction = Direction(new_val)

            if robot.direction == Direction.North:
                self.current_pos = Point(self.current_pos.x, self.current_pos.y - 1)
            elif robot.direction == Direction.East:
                self.current_pos = Point(self.current_pos.x + 1, self.current_pos.y)
            elif robot.direction == Direction.South:
                self.current_pos = Point(self.current_pos.x, self.current_pos.y + 1)
            else:  # robot.direction == Direction.West:
                self.current_pos = Point(self.current_pos.x - 1, self.current_pos.y)

            self.next_ins_is_direction = False
        else:
            self.been_painted.add(self.current_pos)
            if ins:
                self.white_panels.add(self.current_pos)
            else:
                self.white_panels.discard(self.current_pos)

            self.next_ins_is_direction = True


robot = Robot()
args, lines = parse_args_and_get_input()
code_immutable = parse_program(lines[0])

if args.part_one:
    IntComputer(code_immutable, robot.get_current_color, robot.receive_instruction).run()
    print(len(robot.been_painted))
else:
    robot.white_panels.add(Point(0, 0))
    IntComputer(code_immutable, robot.get_current_color, robot.receive_instruction).run()

    paint = ""
    for y in range(8):
        for x in range(80):
            if Point(x, y) in robot.white_panels:
                paint += "#"
            else:
                paint += " "
        paint += "\n"

    print(paint)

