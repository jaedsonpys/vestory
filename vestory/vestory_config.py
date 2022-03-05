import os
import json

HOME = os.getenv('HOME')
CONFIG_FILE = os.path.join(HOME, '.vestoryconfig')
CONFIG = {'author': None, 'author_email': None}


def create_config() -> None:
    _save_config(CONFIG)


def _get_config() -> dict:
    if not os.path.isfile(CONFIG_FILE):
        create_config()
        return CONFIG

    with open(CONFIG_FILE, 'r') as file_r:
        config = json.load(file_r)

    return config


def _save_config(config: dict) -> None:
    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(config, file_w, indent=2, ensure_ascii=False)


def set_author_name(author: str) -> None:
    config = _get_config()
    config['author'] = author
    _save_config(config)


def set_author_email(author_email: str) -> None:
    config = _get_config()
    config['author_email'] = author_email
    _save_config(config)


if __name__ == '__main__':
    create_config()
    set_author_name('Jaedson')
    set_author_email('test@mail.com')
