from leadsheet.chords import parse_chord

def test_structured_slash_chord_preserves_display():
    chord = parse_chord("Fm7/Bb")
    assert (chord.root, chord.kind, chord.bass, chord.display_text) == ("F", "m7", "Bb", "Fm7/Bb")
