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


# class Py0:
#     def __init__(self):
#         if len(sys.argv) < 1:
#             raise ValueError("No arguments passed")

source = ""
line = input()
while len(line) > 0:
    source += line + "\n"
    line = input()
run(source)
