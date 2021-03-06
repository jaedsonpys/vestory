import os

from argeasy import ArgEasy

from .version_control import (InvalidChangeError, add_files, check_repo_exists,
                              decode_change, get_changes, get_files_changed,
                              get_files_tracked, init_repo, join_changes,
                              submit_change)
from .vestory_config import get_author, set_author_email, set_author_name

EXEC_PATH = os.getcwd()


def write_file(filepath: str, content: str) -> None:
    with open(filepath, 'w') as file_w:
        file_w.write(content)


def main():
    parser = ArgEasy(
        description='Controle de versões Vestory.\n'
        'Visite https://github.com/jaedsonpys/vestory para obter ajuda.',
        version='1.2.0',
        project_name='Vestory'
    )

    parser.add_argument('init', 'Init a repo', action='store_true')
    parser.add_argument('add', 'Add files to tracking', action='append')
    parser.add_argument('submit', 'Submit changes', 'append')
    parser.add_argument('log', 'View history of changes', 'store_true')
    parser.add_argument('status', 'View status of files', 'store_true')
    parser.add_argument('join', 'Join changes of files', action='store_true')

    # config
    parser.add_argument('config', 'Add config to Vestory', action='store_true')
    parser.add_flag('--name', 'Set author name')
    parser.add_flag('--email', 'Set author email')

    parser.add_flag('-a', 'Select all files', action='store_true')
    parser.add_flag('-c', 'Comment the change')
    parser.add_flag('-ac', 'Select all files and comment the change')

    args = parser.get_args()
    repo_exists = check_repo_exists()

    if args.version or args.help:
        return None

    if args.config:
        if args.email and args.name:
            set_author_name(args.name)
            set_author_email(args.email)
        elif args.email:
            set_author_email(args.email)
        elif args.name:
            set_author_name(args.name)
        else:
            print('error: use "--name" or "--email" to set config')
    
        return None

    if args.init:
        if repo_exists:
            print(f'\033[31mJá existe um repositório em "{EXEC_PATH}"\033[m')
        else:
            name, email = get_author()
            init_repo(name, email)
            print(f'\033[1;32mNovo repositório inicializado em "{EXEC_PATH}"!\033[m')
    elif repo_exists:
        if args.add is not None:
            if args.a:
                files_to_add = []

                for root, dir, files in os.walk('./'):
                    if not '.vestory' in root:
                        for file in files:
                            files_to_add.append(os.path.join(root, file))
            else:
                files_to_add = args.add

            add_files(files_to_add)
        elif args.submit is not None:
            comment = args.c

            if not get_files_changed():
                print('No changes to be submitted.')
                return None

            if args.a:
                if not comment:
                    print('error: a comment on the change is required. Use "-c."')
                    return None
                files_to_submit = [file for file in get_files_tracked().keys()]
            elif args.ac:
                files_to_submit = [file for file in get_files_tracked().keys()]
                comment = args.ac
            else:
                if not args.submit:
                    print('error: specify the files to be submitted')
                    return None
                files_to_submit = args.submit

            len_files = len(files_to_submit)
            change_id = submit_change(files_to_submit, comment)
            print(f'{len_files} changed (ID: {change_id})')
        elif args.log:
            changes = get_changes()
            changes_list = []
            invalid_changes = []

            for change_id, change_token in changes.items():
                change_info = decode_change(change_token)
                if not change_token:
                    invalid_changes.append(change_id)
                else:
                    changes_list.append((change_id, change_info))
            
            if invalid_changes:
                print('error: invalid changes detected:')
                for i in invalid_changes:
                    print(f'    \033[31mINVALID\033[m: {i}')
                    return None

            # last changes first
            changes_list.reverse()

            for change_id, change_info in changes_list:
                date = change_info.get('date')
                comment = change_info.get('comment')
                author = change_info.get('author')
                author_email = change_info.get('author_email')

                print(f'\033[33m{date} - {change_id}\033[m')
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
                'replace the current files.\033[m')

            while True:
                confirm = input('\033[1m> Do you wish to proceed? [y/n] ').strip().lower()
                if confirm not in ('y', 'n'):
                    print('\033[31mSelect an option between "y" and "n"\033[m')
                    continue
                else:
                    break

            if confirm == 'n':
                return None

            joined_changes = join_changes()

            for filepath, content in joined_changes.items():
                file_lines = [line for line in content.values()]
                write_file(filepath, ''.join(file_lines))
                print(f'\033[32mfile "{filepath}" successfully completed\033[m')
        
            print('\nDone.')
    else:
        print('\033[merror: .vestory repo not found\033[m')

    return None
