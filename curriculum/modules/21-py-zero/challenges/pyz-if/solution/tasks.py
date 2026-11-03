"""Python from Zero 04: if, elif, else."""


def is_even(n):
    return n % 2 == 0


def sign(n):
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"


def band(mhz):
    if mhz < 30:
        return "HF"
    elif mhz < 300:
        return "VHF"
    elif mhz < 3000:
        return "UHF"
    else:
        return "SHF"


def can_listen(has_antenna, has_power):
    return has_antenna and has_power


def largest(a, b, c):
    if a >= b and a >= c:
        return a
    elif b >= c:
        return b
    else:
        return c
