import json
from pathlib import Path
from jsonschema import Draft202012Validator
from .chords import parse_chord
from .models import Song
from .rhythm import derive_slashes

SCHEMA = Path(__file__).parents[2] / "schema" / "song.schema.json"

def validate_data(data: dict) -> Song:
    Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8"))).validate(data)
    song = Song.from_dict(data)
    numbers = [m.number for m in song.measures]
    if numbers != list(range(1, len(numbers) + 1)): raise ValueError("measure numbers must be sequential from 1")
    if any(s.starting_measure not in numbers for s in song.sections): raise ValueError("section starting measure does not exist")
    for measure in song.measures:
        onsets = [h.onset for h in measure.harmony]
        if onsets != sorted(set(onsets)): raise ValueError(f"harmony onsets must be unique and sorted in measure {measure.number}")
        if not onsets or onsets[0] != 0: raise ValueError(f"measure {measure.number} must establish harmony at beat 1")
        for harmony in measure.harmony: parse_chord(harmony.symbol)
        derive_slashes(measure, song.meter)
    return song

def validate_file(path: str | Path) -> Song:
    return validate_data(json.loads(Path(path).read_text(encoding="utf-8")))
