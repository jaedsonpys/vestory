from datetime import datetime
from os import mkdir, path


def _write_file(content: bytes, path: str) -> None:
    with open(path, 'wb') as file_w:
        file_w.write(content)


def init_repo(local: str) -> None:
    """Inicializa um repositório
    vazio.

    :param local: Local do repositório.
    :type local: str
    """

    if not path.isdir(local):
        raise NotADirectoryError('"local" não é um diretório')

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
    vestory_config = {'tracking_files': list(),
                      'author': author,
                      'author_email': author_email,
                      'init_date': init_date}
    
    print(f'Novo repositório criado em "{repo_path}".')


if __name__ == '__main__':
    init_repo('/home/jaedsonpys/Documentos/vestory-project')
