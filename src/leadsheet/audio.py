"""Portable audio ingestion; musical interpretation remains a review step."""

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path

from mutagen.mp3 import MP3, HeaderNotFoundError


@dataclass(frozen=True)
class AudioSource:
    path: str
    sha256: str
    duration_seconds: float
    sample_rate: int
    channels: int
    bitrate: int
    title: str


def inspect_mp3(path: str | Path) -> AudioSource:
    source = Path(path)
    if source.suffix.lower() != ".mp3":
        raise ValueError("audio ingestion currently supports .mp3 files")
    if not source.is_file():
        raise FileNotFoundError(source)
    try:
        audio = MP3(source)
    except HeaderNotFoundError as exc:
        raise ValueError(f"invalid MP3: {source}") from exc
    digest = sha256(source.read_bytes()).hexdigest()
    tags = audio.tags or {}
    tagged_title = tags.get("TIT2")
    title = str(tagged_title) if tagged_title else source.stem
    return AudioSource(str(source.resolve()), digest, round(audio.info.length, 3), audio.info.sample_rate, audio.info.channels, audio.info.bitrate, title)


def create_analysis_draft(path: str | Path) -> dict:
    """Create a reviewable boundary document, never fabricated song data."""
    source = inspect_mp3(path)
    return {
        "format_version": 1,
        "status": "awaiting_musical_analysis",
        "source_audio": asdict(source),
        "musical_analysis": {
            "key": None, "mode": None, "meter": None, "tempo": None,
            "sections": [], "measures": [], "uncertainties": [],
        },
        "approval": {"approved": False, "approved_by": None, "approved_at": None},
    }
