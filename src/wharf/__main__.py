from . import cli
import sys


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    cli.cli()

if __name__ == "__main__":
    main()