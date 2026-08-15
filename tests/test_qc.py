from leadsheet.musicxml import generate
from leadsheet.qc import semantic_qc
import xml.etree.ElementTree as ET

def test_semantic_round_trip(betcha_song, tmp_path):
    path = generate(betcha_song, tmp_path / "score.musicxml")
    assert semantic_qc(betcha_song, path) == []

def test_qc_fails_if_harmony_disappears(betcha_song, tmp_path):
    path = generate(betcha_song, tmp_path / "score.musicxml")
    tree = ET.parse(path); measure = tree.getroot().find("./part/measure"); measure.remove(measure.findall("harmony")[-1]); tree.write(path)
    assert any("harmony mismatch" in error for error in semantic_qc(betcha_song, path))
