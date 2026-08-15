from dataclasses import dataclass
from fractions import Fraction

from .models import Measure, Meter


@dataclass(frozen=True)
class Slash:
    onset: Fraction
    duration: Fraction
    beam: str | None = None


def derive_slashes(measure: Measure, default_meter: Meter) -> tuple[Slash, ...]:
    meter = measure.meter or default_meter
    if meter.beat_type != 4:
        raise ValueError("Milestone 1 supports quarter-note beat units")
    duration = meter.duration_quarters
    onsets = [event.onset for event in measure.harmony]
    if any(p < 0 or p >= duration for p in onsets):
        raise ValueError(f"harmony onset outside measure {measure.number}")
    boundaries = {Fraction(i) for i in range(meter.beats + 1)} | set(onsets)
    points = sorted(boundaries)
    raw = [Slash(a, b - a) for a, b in zip(points, points[1:])]
    result = []
    for slash in raw:
        beam = None
        if slash.duration == Fraction(1, 2):
            if slash.onset.denominator == 1 and any(s.onset == slash.onset + slash.duration and s.duration == slash.duration for s in raw):
                beam = "begin"
            elif slash.onset.denominator == 2 and slash.onset.numerator % 2:
                beam = "end"
        result.append(Slash(slash.onset, slash.duration, beam))
    return tuple(result)
