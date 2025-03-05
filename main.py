from dotenv import load_dotenv
import os
from audio import AudioPipeline

load_dotenv()

import yaml

# Load YAML config
def load_config(config_path="config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
CONFIG = load_config()
CONFIG['HF_TOKEN'] = os.getenv('HF_TOKEN')


audio_file = "/Users/erickshaffer/Music/Audio Hijack/20250303 1509 Recording.mp3"

AudioPipeline(config=CONFIG, audio_file=audio_file).\
    transcribe_with_whisper().\
    align_output().\
    assign_speaker_labels().\
    merge_segements().\
    save()
