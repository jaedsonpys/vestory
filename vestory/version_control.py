from base64 import b64encode
import json
from datetime import datetime
from hashlib import md5
from os import getcwd, mkdir, path
from typing import Final

LOCAL: Final = getcwd()

REPO_PATH: Final = path.join(LOCAL, '.vestory')
CHANGES_DIR: Final = path.join(REPO_PATH, 'changes')
CONFIG_FILE: Final = path.join(REPO_PATH, 'vestory.config.json')


def _write_file(content: str, path: str) -> None:
    with open(path, 'w') as file_w:
        file_w.write(content)


def _update_file(content: str, path: str) -> None:
    with open(path, 'a') as file_w:
        file_w.write(content)


def _get_files_tracked() -> list:
    with open(CONFIG_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    return vestory_config['tracking_files']


def _update_tracked_files(files: list) -> None:
    with open(CONFIG_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['tracking_files'] = files

    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)


def _check_repo_exists() -> bool:
    return path.isdir(REPO_PATH)


def _enumerate_lines(lines: str):
    result = {}

    for i, line in enumerate(lines):
        result[i] = line

    return result


def init_repo() -> None:
    """Inicializa um repositório
    vazio.

    :param local: Local do repositório.
    :type local: str
    """

    if _check_repo_exists():
        print(f'Já existe um repositório em "{REPO_PATH}"')
        return None

    # criando diretório ".vestory"
    mkdir(REPO_PATH)

    # obtendo informações
    author = input('Nome: ').strip()
    author_email = input('Email: ').strip()

    init_date = str(datetime.now())

    # adicionando arquivo de configuração
    vestory_config = {'author': author,
                      'author_email': author_email,
                      'init_date': init_date,
                      'tracking_files': list()}

    # salvando configurações    
    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)
    
    print(f'Novo repositório criado em "{REPO_PATH}".')


def add_files(files: list) -> None:
    """Adiciona os arquivos
    a árvore de rastreamento.

    :param files: Arquivos a serem adicionados.
    :type files: list
    """

    if not _check_repo_exists():
        print('Impossível adicionar arquivos.')
        print('\033[31mNenhum repositório encontrado\033[m')
        return None
    
    tracked_files = _get_files_tracked()
    to_add = list()

    for file in files:
        if file not in tracked_files:
            if path.isfile(file):
                to_add.append(file)
            else:
                print(f'\033[31m"{file}" não encontrado\033[m')

    tracked_files.extend(to_add)
    _update_tracked_files(tracked_files)


def submit_change(files: list, comment: str) -> None:
    """Salva a alteração
    de arquivos.

    :param files: Arquivos a serem submetidos.
    :type files: list
    """

    if not _check_repo_exists():
        print('Impossível adicionar arquivos.')
        print('\033[31mNenhum repositório encontrado\033[m')
        return None

    tracked_files = _get_files_tracked()

    for file in files:
        # ignorando arquivo não rastreado
        if file not in tracked_files:
            continue

        file_history_path = path.join(CHANGES_DIR, md5(file))

        # primeira mudança
        if not path.isfile(file_history_path):
            with open(file, 'r') as file_r:
                file_content = file_r.readlines()

            file_lines = _enumerate_lines(file_content)
            change_info = {'date': str(datetime.now()),
                           'comment': comment,
                           'file': file_lines}

            change_info_json = json.dumps(change_info, ensure_ascii=False)
            change_info_base64 = b64encode(change_info_json.encode())

            _write_file(change_info_base64, file_history_path)


if __name__ == '__main__':
    init_repo()
