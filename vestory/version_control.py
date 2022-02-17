import json
from datetime import datetime
from os import getcwd, mkdir, path

local = getcwd()
repo_path = path.join(local, '.vestory')
config_file = path.join(repo_path, 'vestory.config.json')


def _write_file(content: str, path: str) -> None:
    with open(path, 'w') as file_w:
        file_w.write(content)


def _get_files_tracked() -> list:
    with open(config_file, 'r') as file_r:
        vestory_config = json.load(file_r)

    return vestory_config['tracking_files']


def _update_tracked_files(files: list) -> None:
    with open(config_file, 'r') as file_r:
        vestory_config = json.load(file_r)

    vestory_config['tracking_files'] = files

    with open(config_file, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)


def _check_repo_exists() -> bool:
    return path.isdir(repo_path)


def init_repo() -> None:
    """Inicializa um repositório
    vazio.

    :param local: Local do repositório.
    :type local: str
    """

    if _check_repo_exists():
        print(f'Já existe um repositório em "{repo_path}"')

    # criando diretório ".vestory"
    mkdir(repo_path)

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
    with open(config_file, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)
    
    print(f'Novo repositório criado em "{repo_path}".')


def add_files(files: list) -> None:
    """Adiciona os arquivos
    a árvore de rastreamento.

    :param files: Arquivos a serem adicionados.
    :type files: list
    """

    if not _check_repo_exists():
        print('Impossível adicionar arquivos.')
        print('\033[31mNenhum repositório encontrado\033[m')
    
    tracked_files = _get_files_tracked()
    to_add = list()

    for file in files:
        if file not in tracked_files:
            if path.isfile(file):
                to_add.append(file)
            else:
                print(f'\033[31m"{file}" não encontrado\033[m')

    tracked_files.extend(to_add)


if __name__ == '__main__':
    init_repo()
