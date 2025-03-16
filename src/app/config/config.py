import yaml
import os
from dotenv import load_dotenv
load_dotenv()

# Load YAML config
def load_config(config_path="config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
CONFIG = load_config()
CONFIG['HF_TOKEN'] = os.getenv('HF_TOKEN')