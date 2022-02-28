import json
import os
from base64 import b64decode, b64encode
from datetime import datetime
from hashlib import md5
from os import getcwd, mkdir, path
from random import choice
from string import ascii_letters, digits
from typing import Final, List

from .exceptions import RepoNotExistsError

LOCAL: Final = getcwd()

REPO_PATH: Final = path.join(LOCAL, '.vestory')
CHANGES_DIR: Final = path.join(REPO_PATH, 'changes')
CONFIG_FILE: Final = path.join(REPO_PATH, 'vestory.config.json')


def _generate_id() -> str:
    char = ascii_letters + digits
    return ''.join([i for i in choice(char) for __ in range(32)])


def _update_file(content: str, path: str, new_line: bool = False) -> None:
    with open(path, 'a') as file_w:
        if new_line:
            file_w.write(f'{content}\n')
        else:
            file_w.write(content)


def get_files_tracked() -> dict:
    with open(CONFIG_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    return vestory_config['tracking_files']


def _update_tracked_files(files: dict) -> None:
    with open(CONFIG_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['tracking_files'] = files

    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)


def _check_repo_exists() -> bool:
    return path.isdir(REPO_PATH)


def _enumerate_lines(lines: list) -> dict:
    result = {}

    for i, line in enumerate(lines):
        if isinstance(line, bytes):
            line = line.decode()
        result[str(i)] = line

    return result


def _update_file_hash(filename: str, new_hash: str) -> None:
    with open(CONFIG_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['tracking_files'][filename] = new_hash

    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)


def check_file_has_changed(filename: str) -> bool:
    """Checa se o arquivo foi alterado"""

    if not _check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')

    tracked_files = get_files_tracked()

    if filename in tracked_files:
        with open(filename, 'r') as file_r:
            file_lines = file_r.readlines()

            enum_lines = str(_enumerate_lines(file_lines))
            hash_content = md5(enum_lines.encode()).hexdigest()

        previous_hash = tracked_files.get(filename)
        
        if hash_content != previous_hash:
            return True
        else:
            return False

    return False


def get_files_changed() -> list:
    """Retorna quais arquivos foram alterados"""

    tracked_files = get_files_tracked()
    changed_files = []

    for filepath in tracked_files.keys():
        has_changed = check_file_has_changed(filepath)
        if has_changed:
            changed_files.append(filepath)

    return changed_files


def init_repo(author: str, author_email: str) -> bool:
    """Inicializa um repositório
    vazio.

    :param local: Local do repositório.
    :type local: str
    """

    if _check_repo_exists():
        return False

    # criando diretório ".vestory"
    mkdir(REPO_PATH)
    mkdir(CHANGES_DIR)

    init_date = str(datetime.now())

    # adicionando arquivo de configuração
    vestory_config = {
        'author': author,
        'author_email': author_email,
        'init_date': init_date,
        'tracking_files': dict(),
        'changes': dict()
    }

    # salvando configurações    
    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)

    return True


def add_files(files: list) -> None:
    """Adiciona os arquivos
    a árvore de rastreamento.

    :param files: Arquivos a serem adicionados.
    :type files: list
    """

    if not _check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')
    
    tracked_files = get_files_tracked()
    to_add = dict()

    for file in files:
        if file not in tracked_files:
            if path.isfile(file):
                with open(file, 'rb') as file_r:
                    file_content = file_r.read()

                content_hash = md5(file_content).hexdigest()
                to_add[file] = content_hash
            else:
                print(f'error: "{file}" não encontrado')

    tracked_files.update(to_add)
    _update_tracked_files(tracked_files)


def get_author_info() -> tuple:
    with open(CONFIG_FILE, 'r') as file_r:
        config = json.load(file_r)

    return (config['author'], config['author_email'])


def get_filepath_by_id(file_id: str) -> str:
    last_change = get_file_changes(file_id)[-1]
    filepath = last_change['filepath']
    return filepath


def get_file_changes(filepath: str) -> list:
    """Obtém todas as alterações de um arquivo"""

    file_changes = []
    changes = get_changes()
    
    for change_id, info in changes:
        if info['filepath'] == filepath:
            file_changes.append((change_id, info))

    return file_changes


def get_changes() -> dict:
    """Obtém todas as alterações"""

    with open(CONFIG_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    changes = vestory_config.get('changes')
    return changes


def _add_new_change(
    change_id: str,
    change_info: dict,
    file_lines: str
) -> None:
    changes = get_changes()
    change_filepath = os.path.join(CHANGES_DIR, change_id)
    changes[change_id] = change_info

    with open(CONFIG_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['changes'] = changes
    with open(CONFIG_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, ensure_ascii=False, indent=4)

    with open(change_filepath, 'w') as file_w:
        b64_json = b64encode(file_lines)
        file_w.write(b64_json)


def join_file_changes(file_changes: List[dict]) -> dict:
    """Junta todas as alterações de um arquivo"""

    joined_changes = {}

    for change in file_changes:
        for line, content in change['change'].items():
            joined_changes[line] = content

    return joined_changes


def join_changes() -> dict:
    """Retorna a junção de todas as alterações
    de todos os arquivos."""

    history = get_all_changes()
    joined_changes = {}

    for file_id, changes in history.items():
        joined_changes[file_id] = join_file_changes(changes)

    return joined_changes


def check_diff(joined_changes: dict, current_change: dict) -> dict:
    """Retorna a diferença entre dois arquivos"""

    diff = {}

    # compara as linhas da alteração atual
    # com a junção de todas as mudanças
    # já feitas

    for line, content in current_change.items():
        if not joined_changes.get(line) or joined_changes[line] != content:
            diff[line] = content

    return diff


def submit_change(files: list, comment: str) -> None:
    """Salva a alteração
    de arquivos.

    :param files: Arquivos a serem submetidos.
    :type files: list
    """

    if not _check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')

    tracked_files = get_files_tracked()
    author, author_email = get_author_info()

    for filepath in files:
        # ignorando arquivo não rastreado
        if filepath not in tracked_files:
            continue

        with open(filepath, 'rb') as file_r:
            file_content = file_r.readlines()

        change_id = _generate_id()
        change_path = path.join(CHANGES_DIR, change_id)
        file_lines = json.dumps(_enumerate_lines(file_content))
        hash_lines = md5(file_lines.encode()).hexdigest()

        change_info = {
            'author': author,
            'author_email': author_email,
            'date': str(datetime.now()),
            'comment': comment,
            'hash_lines': hash_lines,
            'filepath': filepath
        }

        all_changes = get_file_changes(change_path)

        if all_changes:
            joined_changes = join_file_changes(all_changes)
            difference = check_diff(joined_changes, file_lines)
            change_info['change'] = difference

        _add_new_change(change_id, change_info, file_lines)
