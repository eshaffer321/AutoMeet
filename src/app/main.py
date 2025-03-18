from app.audio import AudioPipeline
from app.config import CONFIG

audio_file = "/Users/erickshaffer/Music/Audio Hijack/20250312 1600 Recording.mp3"

AudioPipeline(config=CONFIG, audio_file=audio_file).\
    transcribe_with_whisper().\
    align_output().\
    assign_speaker_labels().\
    merge_segments().\
    save()
