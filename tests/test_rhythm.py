from fractions import Fraction
from leadsheet.models import HarmonyEvent, Measure, Meter
from leadsheet.rhythm import derive_slashes

def test_normal_four_four_has_four_quarter_slashes():
    result = derive_slashes(Measure(1, "A", (HarmonyEvent("Cmaj7", Fraction(0)),)), Meter(4, 4))
    assert [s.duration for s in result] == [Fraction(1)] * 4

def test_beat_four_split_has_beamed_eighths(betcha_song):
    result = derive_slashes(betcha_song.measures[0], betcha_song.meter)
    assert [s.duration for s in result] == [Fraction(1), Fraction(1), Fraction(1), Fraction(1, 2), Fraction(1, 2)]
    assert [s.beam for s in result[-2:]] == ["begin", "end"]
