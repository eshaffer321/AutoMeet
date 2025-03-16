import yaml
import os
from dotenv import load_dotenv

# Load environment variables from .env (if available)
load_dotenv()

def load_config(config_path="config/config.yaml"):
    """Load YAML configuration file and allow environment variable overrides."""

    # Default config (used if YAML file is missing)
    default_config = {
        "audio_input_dir": "./audio",
        "output_dir": "./transcripts",
        "local_model_dir": "./model",
        "language": "en",
        "model_size": "large-v2",
        "compute_type": "int8",
        "device": "cpu",
        "batch_size": 16,
        "use_diarization": True
    }

    try:
        with open(config_path, "r") as file:
            yaml_config = yaml.safe_load(file) or {}
    except FileNotFoundError:
        print(f"⚠️ Warning: Config file '{config_path}' not found. Using defaults.")
        yaml_config = {}

    # Merge YAML values with defaults
    config = {**default_config, **yaml_config}

    # Allow environment variable overrides
    for key in config:
        env_value = os.getenv(key.upper())  # Convert key to uppercase to match ENV vars
        if env_value is not None:
            if isinstance(config[key], bool):  # Convert string 'true'/'false' to bool
                config[key] = env_value.lower() == "true"
            elif isinstance(config[key], int):  # Convert int values
                config[key] = int(env_value)
            else:
                config[key] = env_value

    return config

CONFIG = load_config()