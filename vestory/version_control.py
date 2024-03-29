import json
import os
from base64 import b64decode, b64encode
from datetime import datetime
from hashlib import md5
from os import getcwd, mkdir, path
from random import choice
from string import ascii_letters, digits
from typing import Final, Union

from . import integrity
from .exceptions import InvalidChangeError, RepoNotExistsError

LOCAL: Final = getcwd()

REPO_PATH: Final = path.join(LOCAL, '.vestory')
VESTORY_FILE: Final = path.join(REPO_PATH, 'vestory.json')
IGNOREME_PATH: Final = path.join(LOCAL, '.ignoreme')


def _generate_id() -> str:
    char = ascii_letters + digits
    return ''.join([choice(char) for __ in range(32)])


def get_files_tracked() -> dict:
    """Get all monitored files.

    :return: Returns a dictionary with all files.
    :rtype: dict
    """

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
        if not file.startswith('./'):
            file = os.path.join('./', file)
        ignored_files.append(file)

    return ignored_files


def check_ignored(dir_or_file: str) -> bool:
    """Checks if the file/directory is being ignored.

    :param dir_or_file: File or directory.
    :type dir_or_file: str
    :return: Returns True for ignored.
    :rtype: bool
    """

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


def decode_change(change_token: str) -> Union[bool, dict]:
    """Decode a token from a change.

    If the return value is False, it
    means the token is invalid or the key
    is invalid.

    :param change_token: Change token
    :type change_token: str
    :return: Returns the value of the token or False.
    :rtype: Union[bool, dict]
    """
    
    change_info = integrity.decode_without_key(change_token)
    author, author_email = get_author_info()
    repo_key = get_repo_key()

    if change_info['author_email'] == author_email:
        change_info = integrity.decode_token(change_token, repo_key)
        if not change_info:
            return False

    return change_info


def _is_binary(filepath: str) -> bool:
    try:
        with open(filepath, 'r') as file_r:
            file_r.read(1024)
    except UnicodeDecodeError:
        return True

    return False


def check_file_has_changed(filename: str) -> bool:
    """Checks if the file has been changed.
    Checking works through the use of MD5 hash.

    :param filename: Name of the file to be checked.
    :type filename: str
    :raises RepoNotExistsError: non-existent repository
    :return: Returns True if the file has been changed.
    :rtype: bool
    """

    if not check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')

    tracked_files = get_files_tracked()

    if filename in tracked_files:
        previous_hash = tracked_files.get(filename) 

        if _is_binary(filename):
            with open(filename, 'rb') as file_r:
                file_content = file_r.read()

            hash_content = md5(file_content).hexdigest()
        else:
            with open(filename, 'r') as file_r:
                file_lines = file_r.readlines()

                enum_lines = _enumerate_lines(file_lines)
                enum_lines_str = json.dumps(enum_lines)
                hash_content = md5(enum_lines_str.encode()).hexdigest()

        return hash_content != previous_hash
    else:
        return False


def get_files_changed() -> list:
    """Get all changed files.

    :return: Returns a list of files that have changed.
    :rtype: list
    """

    tracked_files = get_files_tracked()
    changed_files = []

    for filepath in tracked_files.keys():
        has_changed = check_file_has_changed(filepath)
        if has_changed:
            changed_files.append(filepath)

    return changed_files


def init_repo(author: str, author_email: str) -> bool:
    """Initializes an empty repository.

    :param local: Repository location.
    :type local: str
    """

    if check_repo_exists():
        return False

    # criando diretório ".vestory"
    mkdir(REPO_PATH)
    init_date = str(datetime.now())

    repo_config = {
        'author': author,
        'author_email': author_email,
        'key': _generate_id(),
        'init_date': init_date,
        'tracking_files': dict(),
        'changes': dict()
    }

    # salvando configurações    
    with open(VESTORY_FILE, 'w') as file_w:
        json.dump(repo_config, file_w, indent=4)

    return True


def add_files(files: list) -> None:
    """Add the files the trace tree.

    :param files: Files to add.
    :type files: list
    """

    if not check_repo_exists():
        raise RepoNotExistsError('Repositório não encontrado')
    
    tracked_files = get_files_tracked()
    to_add = dict()

    for file in files:
        if file not in tracked_files and not check_ignored(file):
            if not file.startswith('./'):
                file = os.path.join('./', file)

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
    """Gets the author information of
    the repository.

    :return: Returns the author's name and email.
    :rtype: tuple
    """

    with open(VESTORY_FILE, 'r') as file_r:
        config = json.load(file_r)

    return (config['author'], config['author_email'])


def get_repo_key() -> str:
    with open(VESTORY_FILE, 'r') as file_r:
        config = json.load(file_r)

    return config['key']


def get_file_changes(_filepath: str) -> list:
    """Get all changes from a file.

    :param _filepath: Filepath
    :type _filepath: str
    :raises InvalidChangeError: If change validation fails.
    :return: Returns a list of file changes.
    :rtype: list
    """

    file_changes = []
    changes = get_changes()
    
    for change_id, token in changes.items():
        change_info = decode_change(token)
        if change_info:
            for filepath, fileinfo in change_info['changed_files'].items():
                if filepath == _filepath:
                    file_changes.append((change_id, fileinfo))
        else:
            raise InvalidChangeError(f'Change "{change_id}" invalid')

    return file_changes


def get_change_info_by_id(change_id: str) -> dict:
    """Gets the information of a change by ID.

    :param change_id: Change ID.
    :type change_id: str
    :raises InvalidChangeError: If change validation fails.
    :return: Returns the change information.
    :rtype: Union[dict, None]
    """

    all_changes = get_changes()
    change_token = all_changes.get(change_id)
    change_info = decode_change(change_token)

    if not change_info:
        raise InvalidChangeError(f'Change "{change_id}" invalid')

    return change_info


def get_changes() -> dict:
    """Gets all changes (not decoded).

    :return: Returns the changes.
    :rtype: dict
    """

    with open(VESTORY_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    changes = vestory_config.get('changes')
    return changes


def get_changes_by_author(author_email: str) -> dict:
    """Gets all changes from a given author (decoded).

    :param author_email: Author's email.
    :type author_email: str
    :raises InvalidChangeError: If change validation fails.
    :return: Returns the changes.
    :rtype: dict
    """

    all_changes = get_changes()
    all_changes_decoded = []

    for change_id, change_token in all_changes.items():
        change_info = decode_change(change_token)
        if change_info:
            if author_email == change_info['author_email']:
                all_changes_decoded.append(change_info)
        else:
            raise InvalidChangeError(f'Change "{change_id}" invalid')

    return all_changes_decoded


def _add_new_change(
    change_id: str,
    change_info: dict
) -> None:
    with open(VESTORY_FILE, 'r') as file_r:
        vestory_config = json.load(file_r)

    repo_key = get_repo_key()
    change_info_token = integrity.create_token(change_info, repo_key)
    vestory_config['changes'][change_id] = change_info_token

    with open(VESTORY_FILE, 'w') as file_w:
        json.dump(vestory_config, file_w, ensure_ascii=False, indent=4)


def join_file_changes(changes: list) -> dict:
    """Merge all changes to a file"""

    joined_changes = {}
    for change_id, file_info in changes:
        content = json.loads(b64decode(file_info['content']))
        for nl, line in content.items():
            joined_changes[nl] = line

    return joined_changes


def join_changes() -> dict:
    """Returns the merge of all changes from all files."""

    changes = get_changes()
    joined_changes = {}

    for change_token in changes.values():
        change_info = integrity.decode_without_key(change_token)
        changed_files = change_info['changed_files']

        for filepath in changed_files.keys():
            file_changes = get_file_changes(filepath)
            joined_changes[filepath] = join_file_changes(file_changes)

    return joined_changes


def check_diff(joined_changes: dict, current_change: dict) -> dict:
    """Returns the difference between two files"""

    diff = {}

    # compara as linhas da alteração atual
    # com a junção de todas as mudanças
    # já feitas

    for line, content in current_change.items():
        if not joined_changes.get(line) or joined_changes[line] != content:
            diff[line] = content

    return diff


def submit_change(files: list, comment: str) -> None:
    """Saves the change to the specified files.

    :param files: Files to be submitted.
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
            file_id = _generate_id()

            if _is_binary(filepath):
                with open(filepath, 'rb') as file_r:
                    file_content = file_r.read()

                hash_file = md5(file_content).hexdigest()
                file_content_b64 = b64encode(file_content)

                changed_files[filepath] = {
                    'file_id': file_id,
                    'hash': hash_file,
                    'content': file_content_b64.decode()
                }
            else:
                with open(filepath, 'r') as file_r:
                    file_content = file_r.readlines()

                file_lines = _enumerate_lines(file_content)
                file_lines_str = json.dumps(file_lines)
                file_lines_b64 = b64encode(file_lines_str.encode()).decode()
                hash_file = md5(file_lines_str.encode()).hexdigest()

                changed_files[filepath] = {
                    'file_id': file_id,
                    'hash': hash_file,
                    'content': file_lines_b64
                }

                all_changes = get_file_changes(filepath)

                if all_changes:
                    joined_changes = join_file_changes(all_changes)

                    difference = check_diff(joined_changes, file_lines)
                    difference_bytes = json.dumps(difference).encode()
                    difference_b64 = b64encode(difference_bytes).decode()
                    changed_files[filepath]['content'] = difference_b64

            _update_file_hash(filepath, hash_file)
            
        change_info['changed_files'] = changed_files
        _add_new_change(change_id, change_info)

    return change_id
