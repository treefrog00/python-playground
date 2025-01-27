import itertools
from typing import List


def looping_take(items: List, count: int):
    taken = 0
    while taken < count:
        for item in items:
            if taken == count:
                return

            yield item
            taken += 1


def ping_pong_take(items: List, count: int):
    taken = 0

    while True:
        for item in itertools.cycle(itertools.chain(items, itertools.islice(reversed(items), 1, len(items) - 1))):
            if taken == count:
                return

            yield item
            taken += 1
