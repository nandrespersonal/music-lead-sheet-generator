from pathlib import Path
import pytest
from leadsheet.validator import validate_file

ROOT = Path(__file__).parents[1]

@pytest.fixture
def betcha_song():
    return validate_file(ROOT / "examples" / "betcha_by_golly_wow" / "song.json")

@pytest.fixture
def betcha_split_measure(betcha_song):
    return next(m for m in betcha_song.measures if [h.symbol for h in m.harmony] == ["Ebmaj7", "Fm7", "Gm7"])
