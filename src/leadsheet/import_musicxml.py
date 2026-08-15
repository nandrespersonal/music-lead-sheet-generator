"""One-time migration support for approved legacy MusicXML charts."""

from fractions import Fraction
from pathlib import Path
import xml.etree.ElementTree as ET


def _pitch(node: ET.Element, prefix: str) -> str:
    step = node.findtext(f"{prefix}-step")
    alter = node.findtext(f"{prefix}-alter")
    return step + ("b" if alter == "-1" else "#" if alter == "1" else "")


def _symbol(harmony: ET.Element) -> str:
    root = _pitch(harmony.find("root"), "root")
    kind = harmony.find("kind")
    text = kind.get("text", "")
    bass = harmony.find("bass")
    return root + text + ("/" + _pitch(bass, "bass") if bass is not None else "")


def import_song(path: str | Path) -> dict:
    root = ET.parse(path).getroot()
    measures = root.findall("./part/measure")
    divisions = int(root.findtext(".//divisions"))
    beats = int(root.findtext(".//beats")); beat_type = int(root.findtext(".//beat-type"))
    fifths = int(root.findtext(".//fifths"))
    major_keys = {-7:"Cb",-6:"Gb",-5:"Db",-4:"Ab",-3:"Eb",-2:"Bb",-1:"F",0:"C",1:"G",2:"D",3:"A",4:"E",5:"B",6:"F#",7:"C#"}
    section_names = {"INTRO", "VERSE 1", "PRE-CHORUS", "CHORUS", "VERSE 2", "PRE-CHORUS 2", "FINAL CHORUS / OUTRO"}
    sections = []; current_section = "UNSPECIFIED"; output_measures = []
    for measure in measures:
        number = int(measure.get("number"))
        words = [(w.text or "").strip() for w in measure.findall(".//direction-type/words") + measure.findall(".//direction-type/rehearsal")]
        for word in words:
            if word in section_names:
                current_section = word; sections.append({"name": word, "starting_measure": number})
        cursor = Fraction(0); harmonies = []
        for child in measure:
            if child.tag == "harmony":
                beat_index = int(cursor); offset = cursor - beat_index
                harmonies.append({"symbol": _symbol(child), "onset": {"beat": beat_index + 1, "offset": f"{offset.numerator}/{offset.denominator}"}, "source": "approved v4 MusicXML"})
            elif child.tag == "note":
                cursor += Fraction(int(child.findtext("duration")), divisions)
        output_measures.append({"number": number, "section": current_section, "harmony": harmonies})
    tempo_node = root.find(".//sound[@tempo]")
    song = {"title": root.findtext("./work/work-title"), "key": major_keys[fifths], "mode": "major", "meter": {"beats": beats, "beat_type": beat_type}, "sections": sections, "measures": output_measures}
    if tempo_node is not None: song["tempo"] = round(float(tempo_node.get("tempo")))
    style = root.findtext(".//measure[@number='1']/direction/direction-type/words")
    if style: song["style"] = style
    return song
