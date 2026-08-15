---
name: music-lead-sheet-generator
description: Convert an approved harmony analysis into validated song.json and deterministic MusicXML lead sheets.
---

# Lead-sheet workflow

Use this repository as the canonical renderer. Analyze source audio into an explicit event map, then create or modify `song.json`; do not hand-edit generated MusicXML as the source of truth.

For MP3 input, run `python -m leadsheet ingest-mp3 INPUT --output build/NAME.analysis.json` first. Keep the resulting draft unapproved until its musical event map has been reviewed.

1. Preserve uncertainty and ask for human clarification when key, chord identity, form, or onset is genuinely ambiguous. Never silently omit or invent a chord.
2. Encode exact onsets using beat plus rational offset and validate the JSON.
3. Generate MusicXML through `python -m leadsheet generate ...`.
4. Run semantic QC and the complete test suite.
5. If MuseScore is installed, import/render the MusicXML and inspect chord placement, slash rhythm, section labels, collisions, and page flow.
6. Make corrections in `song.json` or renderer code and add a regression test for renderer bugs.

The AI/human layer determines musical facts. Repository code deterministically validates, derives slash rhythm, serializes, and checks them. Consult the README and tests for implementation and MuseScore compatibility details.
