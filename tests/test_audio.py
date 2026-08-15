from types import SimpleNamespace
import leadsheet.audio as audio

def test_mp3_ingestion_creates_unapproved_analysis_boundary(tmp_path, monkeypatch):
    source = tmp_path / "song.mp3"; source.write_bytes(b"fake-mp3-for-mocked-decoder")
    fake = SimpleNamespace(info=SimpleNamespace(length=12.3456, sample_rate=44100, channels=2, bitrate=192000), tags=None)
    monkeypatch.setattr(audio, "MP3", lambda path: fake)
    draft = audio.create_analysis_draft(source)
    assert draft["status"] == "awaiting_musical_analysis"
    assert draft["approval"]["approved"] is False
    assert draft["source_audio"]["title"] == "song"
    assert draft["source_audio"]["sha256"]

def test_mp3_ingestion_rejects_other_extensions(tmp_path):
    source = tmp_path / "song.wav"; source.write_bytes(b"x")
    try: audio.inspect_mp3(source)
    except ValueError as error: assert ".mp3" in str(error)
    else: raise AssertionError("non-MP3 input accepted")
