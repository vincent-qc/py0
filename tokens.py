
from enum import Enum


class TokenType(Enum):
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_SQUARE = "["
    RIGHT_SQUARE = "]"
    COMMA = ","
    DOT = "."
    SEMICOLON = ";"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    HASHTAG = "#"

    EQUAL = "="
    EQUAL_EQUAL = "=="
    BANG = "!"
    BANG_EQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    IDENTIFIER = ""
    STRING = ""
    NUMBER = ""

    EOF = ""


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self):
        return f"{self.type.value} {self.lexeme} {self.literal}"


SYNTAX = ['(', ')', '{', '}', '[', ']', '.', ',', ';',
          '+', '-', '*', '/', '=', '>', '<', '!']
