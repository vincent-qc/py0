import os
import sys
from parser.parser import Parser

from interpreter.interpreter import Interpreter
from lexer.lexer import Lexer


def run(source):
    lexer = Lexer(source)
    tokens = lexer.scan()

    print("Tokens:", [token.lexeme for token in tokens])

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(statements)


def main():
    # Check if a filename was provided as a command-line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        # Default to a file in the demo directory
        filename = os.path.join(os.path.dirname(__file__), "demo", "demo.py0")

    try:
        # Read the file content
        with open(filename, "r") as file:
            source = file.read()

        # Run the file content
        run(source)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
