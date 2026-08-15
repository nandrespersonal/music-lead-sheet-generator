from leadsheet.import_musicxml import import_song
from leadsheet.musicxml import generate
from leadsheet.qc import assert_semantic_qc
from leadsheet.validator import validate_data

def test_importer_round_trips_golden_fixture(tmp_path):
    source = __import__("pathlib").Path(__file__).parents[1] / "examples" / "betcha_by_golly_wow" / "expected.musicxml"
    song = validate_data(import_song(source))
    assert len(song.measures) == 64
    assert sum(len(m.harmony) for m in song.measures) == 82
    assert len(song.sections) == 7
    output = generate(song, tmp_path / "roundtrip.musicxml")
    assert_semantic_qc(song, output)
