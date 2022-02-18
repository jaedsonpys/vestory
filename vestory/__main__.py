from argparse import ArgumentParser
from .version_control import init_repo, add_files


def main():
    parser = ArgumentParser()
    parser.add_argument('add', nargs='*', action='append')
    parser.add_argument('init', action='store')

    args = parser.parse_args()
    if args.init:
        init_repo()
    elif args.add:
        add_files(args.add)


main()
