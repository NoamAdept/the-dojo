"""Python Qualification 02: data types and dynamic typing."""


def extract_program(s):
    return s[6:13]


def format_item(item, price):
    return f"Item: {item} | Cost: ${price:.2f}"


def safe_div(a, b):
    ok = all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (a, b))
    if not ok:
        print("Error: both inputs must be numbers")
        return None
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: division by zero")
        return None


def power(base: float, exp: float) -> float:
    return base ** exp


def is_palindrome(text: str) -> bool:
    s = text.replace(" ", "").lower()
    return s == s[::-1]


def clean_numbers(items):
    out = []
    for item in items:
        try:
            out.append(float(item))
        except (TypeError, ValueError):
            continue
    return out


class HexNumber:
    def __init__(self, text: str) -> None:
        self.value = int(text, 16)

    def __int__(self) -> int:
        return self.value

    def __str__(self) -> str:
        return hex(self.value)
