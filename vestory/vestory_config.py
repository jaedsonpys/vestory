import os
import json

HOME = os.getenv('HOME')
CONFIG_FILE = os.path.join(HOME, '.vestoryconfig')


def _get_config() -> None:
    with open(CONFIG_FILE, 'r') as file_r:
        config = json.load(file_r)
    
    return config


def _save_config(config: dict) -> None:
    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(config, file_w, indent=2, ensure_ascii=False)
