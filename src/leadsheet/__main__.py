import argparse
from pathlib import Path
import re
from .musicxml import generate
from .qc import assert_semantic_qc
from .validator import validate_file

def _filename(title): return re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_") + ".musicxml"

def main(argv=None):
    parser = argparse.ArgumentParser(prog="leadsheet"); sub = parser.add_subparsers(dest="command", required=True)
    for name in ("generate", "validate"):
        command = sub.add_parser(name); command.add_argument("song")
    qc = sub.add_parser("qc"); qc.add_argument("song"); qc.add_argument("musicxml")
    args = parser.parse_args(argv); song = validate_file(args.song)
    if args.command == "validate": print(f"valid: {args.song}"); return 0
    if args.command == "qc": assert_semantic_qc(song, args.musicxml); print(f"QC passed: {args.musicxml}"); return 0
    target = Path("build") / _filename(song.title); generate(song, target); assert_semantic_qc(song, target); print(target); return 0

if __name__ == "__main__": raise SystemExit(main())
