#!/usr/bin/env python3
import argparse


def build_parser():
    formatter = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=formatter
    )

    parser.add_argument("task", help="Code insertion task")
    return parser


def run(args):
    print("Hello")


def main():
    parser = build_parser()
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
