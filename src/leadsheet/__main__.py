import argparse
import json
from pathlib import Path
import re
from .musicxml import generate
from .qc import assert_semantic_qc
from .validator import validate_file
from .import_musicxml import import_song
from .audio import create_analysis_draft

def _filename(title): return re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_") + ".musicxml"

def main(argv=None):
    parser = argparse.ArgumentParser(prog="leadsheet"); sub = parser.add_subparsers(dest="command", required=True)
    for name in ("generate", "validate"):
        command = sub.add_parser(name); command.add_argument("song")
    qc = sub.add_parser("qc"); qc.add_argument("song"); qc.add_argument("musicxml")
    migrate = sub.add_parser("import-musicxml"); migrate.add_argument("musicxml"); migrate.add_argument("output")
    ingest = sub.add_parser("ingest-mp3"); ingest.add_argument("mp3"); ingest.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    if args.command == "ingest-mp3":
        Path(args.output).parent.mkdir(parents=True, exist_ok=True); Path(args.output).write_text(json.dumps(create_analysis_draft(args.mp3), indent=2) + "\n", encoding="utf-8"); print(args.output); return 0
    if args.command == "import-musicxml":
        Path(args.output).write_text(json.dumps(import_song(args.musicxml), indent=2) + "\n", encoding="utf-8"); validate_file(args.output); print(args.output); return 0
    song = validate_file(args.song)
    if args.command == "validate": print(f"valid: {args.song}"); return 0
    if args.command == "qc": assert_semantic_qc(song, args.musicxml); print(f"QC passed: {args.musicxml}"); return 0
    target = Path("build") / _filename(song.title); generate(song, target); assert_semantic_qc(song, target); print(target); return 0

if __name__ == "__main__": raise SystemExit(main())
