import sys

from lexer import Lexer


def run(source):
    lexer = Lexer(source)
    tokens = lexer.scan()
    for token in tokens:
        print(token.to_string())


class Py0:
    def __init__(self):
        if len(sys.argv) < 1:
            raise ValueError("No arguments passed")


source = input()
run(source)
