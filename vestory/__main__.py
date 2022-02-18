from argparse import ArgumentParser

import version_control


def main():
    parser = ArgumentParser()
    parser.add_argument('add', nargs='*', action='append')
    parser.add_argument('init', action='store')

    args = parser.parse_args()
    if args.init:
        version_control.init_repo()
    elif args.add:
        version_control.add_files(args.add)


main()
