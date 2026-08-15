from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
import json
from pathlib import Path

from .positions import position_to_offset


@dataclass(frozen=True)
class Meter:
    beats: int
    beat_type: int

    @property
    def duration_quarters(self) -> Fraction:
        return Fraction(self.beats * 4, self.beat_type)


@dataclass(frozen=True)
class HarmonyEvent:
    symbol: str
    onset: Fraction
    bass: str | None = None
    extensions: tuple[str, ...] = ()
    alterations: tuple[str, ...] = ()
    confidence: float | None = None
    source: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "HarmonyEvent":
        return cls(data["symbol"], position_to_offset(data["onset"]), data.get("bass"), tuple(data.get("extensions", ())), tuple(data.get("alterations", ())), data.get("confidence"), data.get("source"))


@dataclass(frozen=True)
class Measure:
    number: int
    section: str
    harmony: tuple[HarmonyEvent, ...]
    meter: Meter | None = None


@dataclass(frozen=True)
class Section:
    name: str
    starting_measure: int
    rehearsal_mark: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class Song:
    title: str
    key: str
    mode: str
    meter: Meter
    measures: tuple[Measure, ...]
    subtitle: str | None = None
    composer: str | None = None
    artist: str | None = None
    tempo: int | None = None
    style: str | None = None
    sections: tuple[Section, ...] = field(default_factory=tuple)
    engraving: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Song":
        meter = Meter(**data["meter"])
        measures = tuple(Measure(m["number"], m["section"], tuple(HarmonyEvent.from_dict(h) for h in m["harmony"]), Meter(**m["meter"]) if "meter" in m else None) for m in data["measures"])
        sections = tuple(Section(**s) for s in data.get("sections", ()))
        optional = {k: data.get(k) for k in ("subtitle", "composer", "artist", "tempo", "style")}
        return cls(data["title"], data["key"], data["mode"], meter, measures, sections=sections, engraving=data.get("engraving", {}), **optional)

    @classmethod
    def load(cls, path: str | Path) -> "Song":
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
