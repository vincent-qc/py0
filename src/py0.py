#!/usr/bin/env python3

import argparse
import os
import sys
from parser.parser import Parser

from interpreter.interpreter import Interpreter
from lexer.lexer import Lexer


def run(source):
    lexer = Lexer(source)
    tokens = lexer.scan()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(statements)


def main():
    parser = argparse.ArgumentParser(
        description="Py0 - A simplified Python-like language interpreter",
        epilog="For more information, visit https://github.com/vincent-qc/py0"
    )

    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the .py0 file to execute"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output during execution"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Py0 v0.1.0",
    )

    args = parser.parse_args()

    if args.file:
        filename = args.file
    else:
        print("Error: No file provided. Use -h for help.")
        sys.exit(1)

    try:
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")

        if not filename.endswith(".py0"):
            print(f"Warning: '{filename}' doesn't have a .py0 extension.")

        with open(filename, "r") as file:
            source = file.read()

        run(source)

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
