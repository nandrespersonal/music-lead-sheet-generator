import xml.etree.ElementTree as ET
from leadsheet.musicxml import generate

def test_eb_slashes_use_bb_without_accidental(betcha_song, tmp_path):
    root = ET.parse(generate(betcha_song, tmp_path / "score.musicxml")).getroot(); notes = root.findall(".//note")
    assert notes and all(n.findtext("pitch/step") == "B" and n.findtext("pitch/alter") == "-1" for n in notes)
    assert not root.findall(".//note/accidental")

def test_harmony_count_and_beams_survive(betcha_song, tmp_path):
    root = ET.parse(generate(betcha_song, tmp_path / "score.musicxml")).getroot()
    assert len(root.findall(".//harmony")) == sum(len(m.harmony) for m in betcha_song.measures) == 82
    assert [b.text for b in root.findall(".//beam")].count("begin") == 4
    assert [b.text for b in root.findall(".//beam")].count("end") == 4

def test_layout_preferences_do_not_change_musical_content(betcha_song, tmp_path):
    from dataclasses import replace
    first = generate(betcha_song, tmp_path / "first.musicxml").read_text(encoding="utf-8")
    second = generate(replace(betcha_song, engraving={"systems_per_page": 99}), tmp_path / "second.musicxml").read_text(encoding="utf-8")
    assert first == second
