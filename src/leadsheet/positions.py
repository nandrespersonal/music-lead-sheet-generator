from fractions import Fraction


def parse_fraction(value: str | int | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def position_to_offset(position: dict) -> Fraction:
    """Convert one-based beat + beat-relative offset to quarter-beat offset."""
    return Fraction(position["beat"] - 1) + parse_fraction(position.get("offset", "0/1"))


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"
