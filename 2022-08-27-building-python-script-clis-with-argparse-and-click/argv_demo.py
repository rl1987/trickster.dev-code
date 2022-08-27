#!/usr/bin/python3

import sys


def main():
    if len(sys.argv) == 1:
        print("Usage:")
        print("{} <arg1> <arg2> ...".format(sys.argv[0]))
        return

    for arg in sys.argv[1:]:
        print(arg)


if __name__ == "__main__":
    main()
