import json
import os
from base64 import b64decode, b64encode
from datetime import datetime
from hashlib import md5
from os import getcwd, mkdir, path
from random import choice
from string import ascii_letters, digits
from typing import Final, Union

from .exceptions import RepoNotExistsError

LOCAL: Final = getcwd()

REPO_PATH: Final = path.join(LOCAL, '.vestory')
VESTORY_FILE: Final = path.join(REPO_PATH, 'vestory.json')
IGNOREME_PATH: Final = path.join(LOCAL, '.ignoreme')


def _generate_id() -> str:
    char = ascii_letters + digits
    return ''.join([choice(char) for __ in range(32)])


def get_files_tracked() -> dict:
    with open(VESTORY_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    return vestory_config['tracking_files']


def _get_files_to_ignore() -> list:
    if not os.path.isfile(IGNOREME_PATH):
        return []

    ignored_files = []
    with open(IGNOREME_PATH) as file_r:
        content = file_r.readlines()

    for file in content:
        file = file.replace('\n', '')
        ignored_files.append(file)

    return ignored_files


def check_ignored(dir_or_file: str) -> bool:
    ignored_files = _get_files_to_ignore()

    if dir_or_file in ignored_files:
        return True
    else:
        for file in ignored_files:
            if file in dir_or_file:
                return True


def _update_tracked_files(files: dict) -> None:
    with open(VESTORY_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['tracking_files'] = files

    with open(VESTORY_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)


def check_repo_exists() -> bool:
    return path.isdir(REPO_PATH)


def _enumerate_lines(lines: list) -> dict:
    result = {}

    for i, line in enumerate(lines):
        if isinstance(line, bytes):
            line = line.decode()
        result[str(i)] = line

    return result


def _update_file_hash(filename: str, new_hash: str) -> None:
    with open(VESTORY_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['tracking_files'][filename] = new_hash

    with open(VESTORY_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)


def check_file_has_changed(filename: str) -> bool:
    """Checa se o arquivo foi alterado"""

    if not check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')

    tracked_files = get_files_tracked()

    if filename in tracked_files:
        with open(filename, 'r') as file_r:
            file_lines = file_r.readlines()

            enum_lines = _enumerate_lines(file_lines)
            enum_lines_str = json.dumps(enum_lines)
            hash_content = md5(enum_lines_str.encode()).hexdigest()

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

    if check_repo_exists():
        return False

    # criando diretório ".vestory"
    mkdir(REPO_PATH)
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
    with open(VESTORY_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)

    return True


def add_files(files: list) -> None:
    """Adiciona os arquivos
    a árvore de rastreamento.

    :param files: Arquivos a serem adicionados.
    :type files: list
    """

    if not check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')
    
    tracked_files = get_files_tracked()
    to_add = dict()

    for file in files:
        if file not in tracked_files and not check_ignored(file):
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
    with open(VESTORY_FILE, 'r') as file_r:
        config = json.load(file_r)

    return (config['author'], config['author_email'])


def get_file_changes(_filepath: str) -> list:
    """Obtém todas as alterações de um arquivo"""

    file_changes = []
    changes = get_changes()
    
    for change_id, info in changes.items():
        for filepath, fileinfo in info['changed_files'].items():
            if filepath == _filepath:
                file_changes.append((change_id, fileinfo))

    return file_changes


def get_change_info_by_id(change_id: str) -> Union[dict, None]:
    all_changes = get_changes()
    return all_changes.get(change_id)


def get_changes() -> dict:
    """Obtém todas as alterações"""

    with open(VESTORY_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    changes = vestory_config.get('changes')
    return changes


def _add_new_change(
    change_id: str,
    change_info: dict
) -> None:
    with open(VESTORY_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['changes'][change_id] = change_info

    with open(VESTORY_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, ensure_ascii=False, indent=4)


def join_file_changes(changes: list) -> dict:
    """Junta todas as alterações de um arquivo"""

    joined_changes = {}
    for change_id, file_info in changes:
        content = json.loads(b64decode(file_info['content']))
        for nl, line in content.items():
            joined_changes[nl] = line

    return joined_changes


def join_changes() -> dict:
    """Retorna a junção de todas as alterações
    de todos os arquivos."""

    changes = get_changes()
    joined_changes = {}

    for change_info in changes.values():
        changed_files = change_info['changed_files']
        for filepath in changed_files.keys():
            file_changes = get_file_changes(filepath)
            joined_changes[filepath] = join_file_changes(file_changes)

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

    if not check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')

    author, author_email = get_author_info()
    change_id = _generate_id()
    changed_files = {}

    change_info = {
        'author': author,
        'author_email': author_email,
        'date': str(datetime.now()),
        'comment': comment,
        'changed_files': dict()
    }

    for filepath in files:
        if check_file_has_changed(filepath):
            with open(filepath, 'rb') as file_r:
                file_content = file_r.readlines()

            file_id = _generate_id()
            file_lines = _enumerate_lines(file_content)
            file_lines_str = json.dumps(file_lines)
            file_lines_b64 = b64encode(file_lines_str.encode()).decode()
            hash_lines = md5(file_lines_str.encode()).hexdigest()

            changed_files[filepath] = {
                'file_id': file_id,
                'hash': hash_lines,
                'content': file_lines_b64
            }

            all_changes = get_file_changes(filepath)

            if all_changes:
                joined_changes = join_file_changes(all_changes)

                difference = check_diff(joined_changes, file_lines)
                difference_bytes = json.dumps(difference).encode()
                difference_b64 = b64encode(difference_bytes).decode()
                changed_files[filepath]['content'] = difference_b64

            _update_file_hash(filepath, hash_lines)
            
        change_info['changed_files'] = changed_files
        _add_new_change(change_id, change_info)

    return change_id
