from fractions import Fraction
from pathlib import Path
import xml.etree.ElementTree as ET
from .models import Song
from .musicxml import DIVISIONS
from .rhythm import derive_slashes

def _name(root, prefix):
    step = root.findtext(f"{prefix}-step"); alter = root.findtext(f"{prefix}-alter")
    return step + ("b" if alter == "-1" else "#" if alter == "1" else "")

def _symbol(harmony):
    root = _name(harmony.find("root"), "root"); text = harmony.find("kind").get("text", ""); bass = harmony.find("bass")
    return root + text + ("/" + _name(bass, "bass") if bass is not None else "")

def semantic_qc(song: Song, xml_path: str | Path) -> list[str]:
    errors = []; root = ET.parse(xml_path).getroot(); xml_measures = root.findall("./part/measure")
    if len(xml_measures) != len(song.measures): errors.append("measure count mismatch")
    for expected, actual in zip(song.measures, xml_measures):
        cursor = Fraction(0); actual_events = []
        for child in actual:
            if child.tag == "harmony": actual_events.append((_symbol(child), cursor))
            elif child.tag == "note": cursor += Fraction(int(child.findtext("duration")), DIVISIONS)
        expected_events = [(h.symbol, h.onset) for h in expected.harmony]
        if actual_events != expected_events: errors.append(f"measure {expected.number} harmony mismatch")
        meter = expected.meter or song.meter
        if cursor != meter.duration_quarters: errors.append(f"measure {expected.number} duration mismatch")
        expected_slashes = derive_slashes(expected, song.meter); notes = actual.findall("note")
        if len(notes) != len(expected_slashes): errors.append(f"measure {expected.number} slash count mismatch")
        if any(note.find("accidental") is not None for note in notes): errors.append(f"measure {expected.number} unexpected slash accidental")
        expected_beams = [s.beam for s in expected_slashes if s.beam]; actual_beams = [n.findtext("beam") for n in notes if n.find("beam") is not None]
        if actual_beams != expected_beams: errors.append(f"measure {expected.number} beam mismatch")
    if [e.text for e in root.findall(".//rehearsal")] != [s.rehearsal_mark or s.name for s in song.sections]: errors.append("section label mismatch")
    return errors

def assert_semantic_qc(song: Song, xml_path: str | Path) -> None:
    errors = semantic_qc(song, xml_path)
    if errors: raise ValueError("; ".join(errors))
