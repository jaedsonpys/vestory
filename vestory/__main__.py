import os
from argeasy import ArgEasy

from .version_control import (
    add_files,
    init_repo,
    submit_change,
    get_all_changes
)

EXEC_PATH = os.getcwd()


def main():
    parser = ArgEasy()
    parser.add_argument('init', 'Init a repo', action='store_true')

    # add argument
    parser.add_argument('add', 'Add files to tracking', action='append')
    parser.add_flag('-a', 'Select all files', action='store_true')

    # submit change
    parser.add_argument('submit', 'Submit changes', 'append')
    parser.add_flag('-c', 'Comment the change') 

    # log
    parser.add_argument('log', 'View history of changes', 'store_true')

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
    elif args.submit is not None:
        comment = args.c

        if args.a:
            files_to_submit = []

            for root, dir, files in os.walk('./'):
                for file in files:
                    files_to_submit.append(os.path.join(root, file))
        else:
            files_to_submit = args.submit

        if not comment:
            print('error: a comment on the change is required. Use "-c."')
            return None

        submit_change(files_to_submit, comment)
    elif args.log:
        history = get_all_changes()
        print('All changes:\n')

        for file_id, changes in history.items():
            for change in changes:
                date = change.get('date')
                comment = change.get('comment')

                author = change.get('author')
                author_email = change.get('author_email')

                hash_file = change.get('hash_file')

                print(f'\033[33m{date} - {hash_file}\033[m')
                print(f'Author: {author} ({author_email})')
                print(f'Comment: {comment}\n')

    return None
