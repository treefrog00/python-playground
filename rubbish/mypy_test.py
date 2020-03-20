from dataclasses import dataclass


@dataclass
class C:
    b: str


def f(c: C):
    g(c.b)


def g(x):
    z = x + 5


def h(x):
    print(x)
    f(x)


def l(x):
    print(x)
    f(3)


f(C("hello"))
h(5)
