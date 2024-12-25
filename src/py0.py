import sys

from lexer import Lexer


def run(source):
    lexer = Lexer(source)
    tokens = lexer.get_tokens()


class Py0:
    def __init__(self):
        if len(sys.argv) < 1:
            raise ValueError("No arguments passed")
