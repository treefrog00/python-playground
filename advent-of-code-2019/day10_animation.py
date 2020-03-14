from random import randint
from time import sleep
from asciimatics.screen import Screen
from day10 import test_part_two_large_input, test_part_two_large_expected_asteroid_order, parse_test, get_order_of_destruction


def asciimatics_demo(screen):
    while True:
        screen.print_at('Hello world!',
                        randint(0, screen.width), randint(0, screen.height),
                        colour=randint(0, screen.colours - 1),
                        bg=randint(0, screen.colours - 1))
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()


def run_demo():
    Screen.wrapper(asciimatics_demo)


def day10_animation(screen):
    data, expected_order = test_part_two_large_input, test_part_two_large_expected_asteroid_order
    asteroids, station = parse_test(data)
    destroy_order = get_order_of_destruction(asteroids, station)

    for asteroid in asteroids:
        screen.print_at("#",
                        asteroid.x, asteroid.y + 1,
                        colour=randint(0, screen.colours - 1),
                        bg=Screen.COLOUR_BLACK)
    screen.print_at("X",
                    station.x, station.y + 1,
                    colour=Screen.COLOUR_RED,
                    bg=Screen.COLOUR_BLACK)

    count = 0
    while True and destroy_order:
        destroyed = destroy_order.pop(0)
        count += 1
        screen.print_at(" ",
                        destroyed.asteroid.x, destroyed.asteroid.y + 1,
                        colour=Screen.COLOUR_CYAN,
                        bg=Screen.COLOUR_CYAN)
        screen.print_at(str(count) + "  ",
                        0, 0,
                        colour=Screen.COLOUR_WHITE,
                        bg=Screen.COLOUR_BLACK)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        sleep(0.01)
        screen.refresh()

    while True:
        sleep(0.1)


def run_day10_animate():
    Screen.wrapper(day10_animation)


if __name__ == "__main__":
    run_day10_animate()
