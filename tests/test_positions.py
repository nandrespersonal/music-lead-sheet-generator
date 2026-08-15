from fractions import Fraction
from leadsheet.positions import position_to_offset

def test_beat_four_and_is_exact():
    assert position_to_offset({"beat": 4, "offset": "1/2"}) == Fraction(7, 2)
