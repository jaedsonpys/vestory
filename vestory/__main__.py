import os
from argeasy import ArgEasy

from version_control import add_files, init_repo

EXEC_PATH = os.getcwd()


def main():
    parser = ArgEasy()
    parser.add_argument('init', 'Init a repo', action='store_true')

    # add argument
    parser.add_argument('add', 'Add files to tracking', action='append')
    parser.add_flag('-a', 'Select all files', action='store_true')    

    args = parser.get_args()

    if args.init:
        # test informations
        name = 'Elliot'
        email = 'elliot@protonmail.com'

        result = init_repo(name, email)

        if not result:
            print(f'\033[31mJá existe um repositório em "{EXEC_PATH}"\033[m')
            return None
        
        print(f'\033[1;32mNovo repositório inicializado em "{EXEC_PATH}"!\033[m')
    elif args.add is not None:
        if args.a:
            files_to_add = []

            for root, dir, files in os.walk('./'):
                for file in files:
                    files_to_add.append(os.path.join(root, file))
        else:
            files_to_add = args.add

        add_files(files_to_add)


main()
