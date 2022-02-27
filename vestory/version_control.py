import json
from base64 import b64decode, b64encode
from datetime import datetime
from hashlib import md5
from os import getcwd, mkdir, path
from typing import Final, List

from .exceptions import RepoNotExistsError

LOCAL: Final = getcwd()

REPO_PATH: Final = path.join(LOCAL, '.vestory')
CHANGES_DIR: Final = path.join(REPO_PATH, 'changes')
CONFIG_FILE: Final = path.join(REPO_PATH, 'vestory.config.json')


def _write_file(content: str, path: str) -> None:
    with open(path, 'w') as file_w:
        file_w.write(content)


def _update_file(content: str, path: str, new_line: bool = False) -> None:
    with open(path, 'a') as file_w:
        if new_line:
            file_w.write(f'{content}\n')
        else:
            file_w.write(content)


def _get_files_tracked() -> dict:
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

    tracked_files = _get_files_tracked()

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
    vestory_config = {'author': author,
                      'author_email': author_email,
                      'init_date': init_date,
                      'tracking_files': dict()}

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
    
    tracked_files = _get_files_tracked()
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


def get_file_changes(file_id: str) -> list:
    """Obtém todas as alterações de um arquivo"""

    file_history_path = path.join(CHANGES_DIR, file_id)
    with open(file_history_path, 'r') as file_r:
        file_content = file_r.readlines()

    history = []

    for line in file_content:
        change_info = json.loads(b64decode(line))
        history.append(change_info)

    return history


def join_changes(all_changes: List[dict]) -> dict:
    """Junta todas as alterações de um arquivo"""

    joined_changes = {}

    for change in all_changes:
        for line, content in change['file'].items():
            joined_changes[line] = content

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

    tracked_files = _get_files_tracked()

    for file in files:
        # ignorando arquivo não rastreado
        if file not in tracked_files:
            continue

        hash_file_path = md5(file.encode()).hexdigest()
        file_history_path = path.join(CHANGES_DIR, hash_file_path)

        with open(file, 'rb') as file_r:
            file_content = file_r.readlines()

        file_lines = _enumerate_lines(file_content)
        hash_file = md5(str(file_lines).encode()).hexdigest()

        change_info = {'author': '',
                        'author_email': '',
                        'date': str(datetime.now()),
                        'comment': comment,
                        'hash_file': hash_file,
                        'file': file_lines}

        if path.isfile(file_history_path):
            all_changes = get_file_changes(hash_file_path)
            joined_changes = join_changes(all_changes)
            difference = check_diff(joined_changes, file_lines)

            change_info['file'] = difference

        change_info_json = json.dumps(change_info, ensure_ascii=False).encode()
        change_info_base64 = b64encode(change_info_json).decode()

        _update_file(change_info_base64, file_history_path, new_line=True)
        _update_file_hash(file, hash_file)
