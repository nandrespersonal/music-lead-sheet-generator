from leadsheet.chords import parse_chord

def test_structured_slash_chord_preserves_display():
    chord = parse_chord("Fm7/Bb")
    assert (chord.root, chord.kind, chord.bass, chord.display_text) == ("F", "m7", "Bb", "Fm7/Bb")

def test_no_chord_is_structured_without_fabricated_root():
    chord = parse_chord("N.C.")
    assert (chord.root, chord.kind, chord.display_text) == (None, "none", "N.C.")
