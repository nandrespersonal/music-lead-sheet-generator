# Music Lead Sheet Generator

A deterministic renderer for rhythm-section lead sheets. Human or AI musical analysis decides **what** the music is and records it in canonical `song.json`; this package decides **how** those approved events are represented in MusicXML.

The renderer never transcribes audio and never silently moves or drops harmony events.

## Pipeline

`song.json -> schema/semantic validation -> rhythm derivation -> MusicXML -> semantic QC -> MuseScore`

Musical positions use exact rational values. A position has a one-based `beat` and a fractional `offset`; beat 4-and is `{ "beat": 4, "offset": "1/2" }`. Internally, measure offsets are `Fraction` values measured in quarter-note beats.

## Install and use

```console
python -m pip install -e .[dev]
python -m leadsheet validate examples/betcha_by_golly_wow/song.json
python -m leadsheet generate examples/betcha_by_golly_wow/song.json
python -m leadsheet qc examples/betcha_by_golly_wow/song.json build/Betcha_By_Golly_Wow.musicxml
pytest
```

The minimal Betcha fixture deliberately contains only musical facts available with confidence. It is not a fabricated reconstruction of the full chart.

## Architecture

- `models.py` owns the canonical musical model.
- `positions.py` parses exact positions.
- `rhythm.py` derives the smallest slash subdivision needed to expose harmony attacks.
- `chords.py` parses common structured chord fields while retaining display text.
- `musicxml.py` serializes musical facts.
- `engraving/musescore.py` isolates MuseScore import compatibility.
- `validator.py` checks JSON Schema plus musical invariants.
- `qc.py` semantically compares generated MusicXML with its source song.

Rhythmic slashes are notes with slash noteheads, not rests. In Eb major, MuseScore can show a bogus cancellation natural if a slash at the B staff position is encoded as unpitched B-natural. The compatibility layer therefore chooses a display pitch consistent with the key signature (Bb in Eb major) and emits no `<accidental>` element. This pitch is an engraving carrier, not a performed pitch.

## Current limitations and roadmap

Milestone 1 supports simple meters whose beat unit is a quarter note, exact harmony onsets, structured common chord qualities, section rehearsal marks, deterministic MusicXML, and semantic round-trip checks. Tuplets, pickups, repeats/endings, changing keys, advanced chord alterations, automatic layout QC, audio transcription, and MuseScore PDF/MSCZ invocation remain future work. MuseScore is intentionally not required by core tests.

Complete approved transcriptions should be imported into `song.json`, validated, rendered, and reviewed; missing musical facts must be resolved by a musician rather than guessed.
Deterministic MusicXML lead-sheet generator and MuseScore workflow
