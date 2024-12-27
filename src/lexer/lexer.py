from typing import List

from lexer.tokens import RESERVED, SYNTAX, Token, TokenType
from util.errors import error


def is_alpha(c: str):
    return c.isalpha() or c == '_'


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def lex_syntax(self):
        cur = self.peek()
        next = self.peek(1)
        if cur == '=' and next == '=':
            self.advance()
            return Token(TokenType.EQUAL_EQUAL, cur, None, self.line)
        if cur == '>' and next == '=':
            self.advance()
            return Token(TokenType.GREATER_EQUAL, cur, None, self.line)
        if cur == '<' and next == '=':
            self.advance()
            return Token(TokenType.LESS_EQUAL, cur, None, self.line)
        if cur == '!' and next == '=':
            self.advance()
            return Token(TokenType.BANG_EQUAL, cur, None, self.line)
        return Token(TokenType(cur), cur, None, self.line)

    def lex_string(self) -> Token:
        delimeter = self.peek()
        self.advance()
        res = ""
        while self.peek() != delimeter:
            if self.peek() == '\n' or self.end_of_source(1):
                error(self.line, "Unclosed string")
            res += self.peek()
            self.advance()
        return Token(TokenType.STRING, f"{delimeter}{res}{delimeter}", res, self.line)

    def lex_number(self) -> Token:
        res = ""
        while self.peek().isdigit():
            res += self.peek()
            self.advance()
        if self.peek() == '.' and self.peek(1).isdigit():
            res += self.peek()
            self.advance()
            while self.peek().isdigit():
                res += self.peek()
                self.advance()
        self.advance(-1)
        return Token(TokenType.NUMBER, res, float(res), self.line)

    def lex_identifier(self) -> Token:
        res = ""
        while is_alpha(self.peek()):
            res += self.peek()
            self.advance()
        self.advance(-1)
        if res in RESERVED:
            return Token(TokenType(res), res, None, self.line)
        else:
            return Token(TokenType.IDENTIFIER, res, None, self.line)

    def scan(self) -> List[Token]:
        tokens = []
        while not self.end_of_source():
            cur = self.peek()

            # Skip the entire line after comments
            if cur == '#':
                while not self.end_of_source and self.peek() != '\n':
                    self.advance()
                self.line += 1

            # Increase line count on newline
            elif cur == '\n':
                self.line += 1

            # Check for syntactical lexemes
            elif cur in SYNTAX:
                tokens.append(self.lex_syntax())

            # Check for string literal lexemes
            elif cur == '"' or cur == '\'':
                tokens.append(self.lex_string())

            # Check for numerical literal lexemes
            elif cur.isdigit():
                tokens.append(self.lex_number())

            # Check for identifiers
            elif is_alpha(cur):
                tokens.append(self.lex_identifier())

            # Check blank characters
            elif cur == ' ' or cur == '\t':
                pass

            # Error on illegal characters
            else:
                error(self.line, f"Unidentified character: {cur}")

            # Continue to next character
            self.advance()

        tokens.append(Token(TokenType.EOF, "", None, self.line))
        return tokens

    def peek(self, offset=0) -> str:
        if self.end_of_source(offset):
            return '\0'
        return self.source[self.pos + offset]

    def advance(self, offset=1):
        self.pos += offset

    def end_of_source(self, offset=0) -> bool:
        return self.pos + offset >= 0 and self.pos + offset >= len(self.source)
