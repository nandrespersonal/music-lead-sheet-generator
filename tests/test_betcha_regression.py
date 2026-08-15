from leadsheet.musicxml import generate
from leadsheet.qc import assert_semantic_qc
from fractions import Fraction

def test_betcha_known_measure_regression(betcha_song, betcha_split_measure, tmp_path):
    path = generate(betcha_song, tmp_path / "betcha.musicxml"); assert_semantic_qc(betcha_song, path); text = path.read_text(encoding="utf-8")
    assert [(h.symbol, h.onset) for h in betcha_split_measure.harmony] == [("Ebmaj7", Fraction(0)), ("Fm7", Fraction(3)), ("Gm7", Fraction(7, 2))]
    assert "<accidental" not in text and 'print-object="no"' not in text
