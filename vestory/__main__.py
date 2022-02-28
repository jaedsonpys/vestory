import os
from argeasy import ArgEasy

from .version_control import (
    add_files,
    get_files_changed,
    init_repo,
    submit_change,
    get_all_changes,
    join_changes,
    get_filepath_by_id
)

EXEC_PATH = os.getcwd()


def main():
    parser = ArgEasy()

    parser.add_argument('init', 'Init a repo', action='store_true')
    parser.add_argument('add', 'Add files to tracking', action='append')
    parser.add_argument('submit', 'Submit changes', 'append')
    parser.add_argument('log', 'View history of changes', 'store_true')
    parser.add_argument('status', 'View status of files', 'store_true')
    parser.add_argument('join', 'Join changes of files', action='store_true')

    parser.add_flag('-a', 'Select all files', action='store_true')
    parser.add_flag('-c', 'Comment the change')

    args = parser.get_args()

    if args.init:
        # test informations
        name = 'Elliot'
        email = 'elliot@protonmail.com'

        result = init_repo(name, email)

        if not result:
            print(f'\033[31mJá existe um repositório em "{EXEC_PATH}"\033[m')
        else:
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
        if args.ac:
            files_to_submit = []
            comment = args.ac

            for root, dir, files in os.walk('./'):
                for file in files:
                    files_to_submit.append(os.path.join(root, file))
        else:
            comment = args.c
            if args.a:
                files_to_submit = []

                for root, dir, files in os.walk('./'):
                    if '.vestory/' not in root:
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
    elif args.status:
        changed_files = get_files_changed()

        if not changed_files:
            print('\033[32mno changes detected\033[m')
        else:
            print('files to submit:')
            for file in changed_files:
                print(f'\033[31m    changed: {file}\033[m')

        print('\nuse "vestory submit -a" to submit changes.')
        print('to add files, use "vestory add".')
    elif args.join:
        print('\033[33mwarning: the "join" command will'
              'replace the current files.\033[m\n')

        while True:
            confirm = input('> Do you wish to proceed? [y/n] ').strip().lower()
            if confirm not in ('y', 'n'):
                print('\033[31mSelect an option between "y" and "n"\033[m')
                continue
            else:
                break

        if confirm == 'n':
            return None

        joined_changes = join_changes()

        for file_id, content in joined_changes.items():
            filepath = get_filepath_by_id(file_id)
            file_lines = []

            for line in content.values():
                file_lines.append(line)

            with open(filepath, 'w') as file_w:
                file_w.write(''.join(file_lines))

            print(f'\033[32mfile "{filepath}" successfully completed\033[m')
    
        print('\nDone.')

    return None
