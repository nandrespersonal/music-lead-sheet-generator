from leadsheet.musicxml import generate
from leadsheet.qc import assert_semantic_qc

def test_betcha_known_measure_regression(betcha_song, tmp_path):
    path = generate(betcha_song, tmp_path / "betcha.musicxml"); assert_semantic_qc(betcha_song, path); text = path.read_text(encoding="utf-8")
    assert 'text="maj7"' in text and text.count('text="m7"') == 2
    assert "<accidental" not in text and 'print-object="no"' not in text
