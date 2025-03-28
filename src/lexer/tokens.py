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
    COLON = ":"
    SEMICOLON = ";"
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    MOD = "%"
    HASHTAG = "#"
    AMPERSAND = "&"
    PIPE = "|"
    XOR = "^"

    EQUAL = "="
    EQUAL_EQUAL = "=="
    PLUS_EQUAL = "+="
    MINUS_EQUAL = "-="
    BANG = "!"
    BANG_EQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    INDENT = "_INDENT"
    UNDENT = "_UNDENT"

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
    IN = "in"
    RETURN = "return"
    TRUE = "True"
    FALSE = "False"

    STR = "str"
    BOOL = "bool"
    INT = "int"
    FLOAT = "float"
    LIST = "List"
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


SYNTAX = ['(', ')', '{', '}', '[', ']', '.', ',', ':',
          '+', '-', '*', '/', '%', '=', '>', '<', '!',
          '&', '|', '^', ';']

TYPES = ["str", "int", "float", "bool", "List", "None"]

RESERVED = ["and", "or", "class", "if", "elif",
            "else", "self", "def", "while", "for", "in", "return", "True", "False"]

SYNCHRONIZATION = [TokenType.CLASS, TokenType.DEF,
                   TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.RETURN]
