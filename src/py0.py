import sys
from parser import Parser

from interpreter import Interpreter
from lexer import Lexer
from util import ExpressionPrinter


def run(source):
    lexer = Lexer(source)
    tokens = lexer.scan()
    parser = Parser(tokens)
    result = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(result)


# class Py0:
#     def __init__(self):
#         if len(sys.argv) < 1:
#             raise ValueError("No arguments passed")

source = input()
run(source)
