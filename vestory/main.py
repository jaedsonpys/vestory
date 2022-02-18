from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('init', action='store_true')
    parser.add_argument('add', nargs='*', action='append')

    args = parser.parse_args()


main()
