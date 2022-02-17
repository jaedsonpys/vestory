import json
from datetime import datetime
from os import getcwd, mkdir, path


def _write_file(content: str, path: str) -> None:
    with open(path, 'w') as file_w:
        file_w.write(content)


def _check_repo_exists() -> bool:
    local = getcwd()
    repo_path = path.join(local, '.vestory')

    return path.isdir(repo_path)


def init_repo() -> None:
    """Inicializa um repositório
    vazio.

    :param local: Local do repositório.
    :type local: str
    """

    local = getcwd()

    # criando diretório ".vestory"
    repo_path = path.join(local, '.vestory')
    
    try:
        mkdir(repo_path)
    except FileExistsError:
        print(f'Já existe um repositório em "{repo_path}".')
        return None

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
    config_file = path.join(repo_path, 'vestory.config.json')
    
    with open(config_file, 'w') as file_w:
        json.dump(vestory_config, file_w, indent=4)
    
    print(f'Novo repositório criado em "{repo_path}".')


if __name__ == '__main__':
    init_repo()
