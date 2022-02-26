import os
from argparse import ArgumentParser

from version_control import add_files, init_repo

EXEC_PATH = os.getcwd()


def main():
    parser = ArgumentParser()
    parser.add_argument('add', nargs='*', action='append')
    parser.add_argument('-i', action='store_true')  # -i is used to init repo

    args = parser.parse_args()
    
    if args.i:
        # test informations
        name = 'Elliot'
        email = 'elliot@protonmail.com'

        result = init_repo(name, email)

        if not result:
            print(f'\033[31mJá existe um repositório em "{EXEC_PATH}"\033[m')
            return None
        
        print(f'\033[1;32mNovo repositório inicializado em "{EXEC_PATH}"!\033[m')
    elif args.add:
        to_add = args.add
        add_files(to_add)


main()
