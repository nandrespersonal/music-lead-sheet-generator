from dataclasses import dataclass


@dataclass(frozen=True)
class DisplayPitch:
    step: str
    alter: int
    octave: int = 4


_FIFTHS = {"Cb": -7, "Gb": -6, "Db": -5, "Ab": -4, "Eb": -3, "Bb": -2, "F": -1, "C": 0, "G": 1, "D": 2, "A": 3, "E": 4, "B": 5, "F#": 6, "C#": 7}
_FLAT_ORDER = "BEADGCF"
_SHARP_ORDER = "FCGDAEB"


def key_fifths(key: str, mode: str) -> int:
    if mode == "minor":
        relative_major = {"A": "C", "E": "G", "B": "D", "F#": "A", "C#": "E", "G#": "B", "D#": "F#", "A#": "C#", "D": "F", "G": "Bb", "C": "Eb", "F": "Ab", "Bb": "Db", "Eb": "Gb", "Ab": "Cb"}
        key = relative_major[key]
    return _FIFTHS[key]


def choose_slash_display_pitch(key: str, mode: str, desired_step: str = "B") -> DisplayPitch:
    fifths = key_fifths(key, mode)
    altered = _SHARP_ORDER[:fifths] if fifths > 0 else _FLAT_ORDER[:abs(fifths)]
    alter = 1 if fifths > 0 and desired_step in altered else -1 if fifths < 0 and desired_step in altered else 0
    return DisplayPitch(desired_step, alter)
