from pathlib import Path
import pytest
from leadsheet.validator import validate_file

ROOT = Path(__file__).parents[1]

@pytest.fixture
def betcha_song():
    return validate_file(ROOT / "examples" / "betcha_by_golly_wow" / "song.json")
