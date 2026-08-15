from fractions import Fraction
from pathlib import Path
import xml.etree.ElementTree as ET
from .chords import KIND_MAP, parse_chord
from .engraving.musescore import choose_slash_display_pitch, key_fifths
from .models import Song
from .rhythm import derive_slashes

DIVISIONS = 4
TYPE = {Fraction(1): "quarter", Fraction(1, 2): "eighth", Fraction(1, 4): "16th", Fraction(2): "half", Fraction(4): "whole"}

def _pitch_parts(name): return name[0], -1 if name.endswith("b") else 1 if name.endswith("#") else 0

def _harmony(parent, symbol):
    chord = parse_chord(symbol); harmony = ET.SubElement(parent, "harmony"); root = ET.SubElement(harmony, "root")
    step, alter = _pitch_parts(chord.root); ET.SubElement(root, "root-step").text = step
    if alter: ET.SubElement(root, "root-alter").text = str(alter)
    kind = ET.SubElement(harmony, "kind", {"text": chord.kind}); kind.text = KIND_MAP.get(chord.kind, "other")
    if chord.bass:
        bass = ET.SubElement(harmony, "bass"); step, alter = _pitch_parts(chord.bass); ET.SubElement(bass, "bass-step").text = step
        if alter: ET.SubElement(bass, "bass-alter").text = str(alter)

def to_element(song: Song) -> ET.Element:
    score = ET.Element("score-partwise", {"version": "4.0"}); work = ET.SubElement(score, "work"); ET.SubElement(work, "work-title").text = song.title
    part_list = ET.SubElement(score, "part-list"); score_part = ET.SubElement(part_list, "score-part", {"id": "P1"}); ET.SubElement(score_part, "part-name").text = "Lead Sheet"
    part = ET.SubElement(score, "part", {"id": "P1"}); section_starts = {s.starting_measure: (s.rehearsal_mark or s.name) for s in song.sections}; pitch = choose_slash_display_pitch(song.key, song.mode)
    for index, measure in enumerate(song.measures):
        node = ET.SubElement(part, "measure", {"number": str(measure.number)}); meter = measure.meter or song.meter
        if index == 0 or measure.meter:
            attrs = ET.SubElement(node, "attributes"); ET.SubElement(attrs, "divisions").text = str(DIVISIONS)
            if index == 0:
                key = ET.SubElement(attrs, "key"); ET.SubElement(key, "fifths").text = str(key_fifths(song.key, song.mode))
            time = ET.SubElement(attrs, "time"); ET.SubElement(time, "beats").text = str(meter.beats); ET.SubElement(time, "beat-type").text = str(meter.beat_type)
            if index == 0:
                clef = ET.SubElement(attrs, "clef"); ET.SubElement(clef, "sign").text = "G"; ET.SubElement(clef, "line").text = "2"
        if measure.number in section_starts:
            direction = ET.SubElement(node, "direction", {"placement": "above"}); dtype = ET.SubElement(direction, "direction-type"); ET.SubElement(dtype, "rehearsal").text = section_starts[measure.number]
        events = {h.onset: h for h in measure.harmony}
        for slash in derive_slashes(measure, song.meter):
            if slash.onset in events: _harmony(node, events[slash.onset].symbol)
            note = ET.SubElement(node, "note"); p = ET.SubElement(note, "pitch"); ET.SubElement(p, "step").text = pitch.step
            if pitch.alter: ET.SubElement(p, "alter").text = str(pitch.alter)
            ET.SubElement(p, "octave").text = str(pitch.octave); ticks = slash.duration * DIVISIONS
            if ticks.denominator != 1 or slash.duration not in TYPE: raise ValueError(f"unsupported slash duration {slash.duration}")
            ET.SubElement(note, "duration").text = str(ticks.numerator); ET.SubElement(note, "type").text = TYPE[slash.duration]; ET.SubElement(note, "notehead").text = "slash"
            if slash.beam: ET.SubElement(note, "beam", {"number": "1"}).text = slash.beam
    return score

def generate(song: Song, path: str | Path) -> Path:
    target = Path(path); target.parent.mkdir(parents=True, exist_ok=True); tree = ET.ElementTree(to_element(song)); ET.indent(tree, space="  "); tree.write(target, encoding="utf-8", xml_declaration=True); return target
