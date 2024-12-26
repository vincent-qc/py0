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
    COLON = ":"
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

    IDENTIFIER = "_IDENTIFIER"  # remove these
    STRING = "_STRING"
    NUMBER = "_NUMBER"

    AND = "and"
    OR = "or"
    CLASS = "class"
    IF = "if"
    ELIF = "elif"
    ELSE = "else"
    SELF = "self"
    DEF = "def"
    WHILE = "while"
    FOR = "for"
    RETURN = "return"
    TRUE = "True"
    FALSE = "False"
    NONE = "None"

    EOF = "EOF"


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal: object, line: int):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self):
        return f"{self.type.value} {self.lexeme} {self.literal}"


SYNTAX = ['(', ')', '{', '}', '[', ']', '.', ',', ';', ':',
          '+', '-', '*', '/', '=', '>', '<', '!']

RESERVED = ["and", "or", "class", "if", "elif",
            "else", "self", "def", "while", "for", "return", "True", "False", "None"]

SYNCHRONIZATION = [TokenType.CLASS, TokenType.DEF,
                   TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.RETURN]
