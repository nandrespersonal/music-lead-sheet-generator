from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Chord:
    root: str
    kind: str
    bass: str | None
    display_text: str


_CHORD = re.compile(r"^(?P<root>[A-G](?:b|#)?)(?P<kind>[^/]*)?(?:/(?P<bass>[A-G](?:b|#)?))?$")


def parse_chord(symbol: str) -> Chord:
    match = _CHORD.fullmatch(symbol)
    if not match:
        raise ValueError(f"unsupported chord symbol: {symbol}")
    return Chord(match["root"], match["kind"] or "", match["bass"], symbol)


KIND_MAP = {"": "major", "m": "minor", "m7": "minor-seventh", "7": "dominant", "maj7": "major-seventh", "maj9": "major-ninth"}
