import sys
from parser import Parser

from grammar.expression import ExpressionPrinter
from lexer import Lexer


def run(source):
    lexer = Lexer(source)
    tokens = lexer.scan()
    parser = Parser(tokens)
    result = parser.parse()
    print(result)
    printer = ExpressionPrinter()
    print(printer.visit_binary(result))


# class Py0:
#     def __init__(self):
#         if len(sys.argv) < 1:
#             raise ValueError("No arguments passed")

source = input()
run(source)
