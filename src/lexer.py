from typing import List, Optional

from tokens import SYNTAX, Token, TokenType


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def lex_syntax(self, cur: str):
        if cur == '=' and self.match('='):
            return Token(TokenType.EQUAL_EQUAL, cur, None, self.line)
        if cur == '>' and self.match('='):
            return Token(TokenType.GREATER_EQUAL, cur, None, self.line)
        if cur == '<' and self.match('='):
            return Token(TokenType.LESS_EQUAL, cur, None, self.line)
        if cur == '!' and self.match('='):
            return Token(TokenType.BANG_EQUAL, cur, None, self.line)
        return Token(TokenType(cur), cur, None, self.line)

    def lex_string(self):
        eol = self.source.find('\n', self.pos)
        eol = eol if eol != -1 else len(self.source)
        next_quote = self.source.find('"', self.pos, eol)
        if next_quote == -1:
            raise SyntaxError("Unclosed string literal")
        else:
            substr = self.source[self.pos:next_quote]
            return Token(TokenType.STRING, f"\"{substr}\"", substr, self.line)

    def lex_number(self, cur):
        res = cur
        used_point = False
        while not self.end_of_source():
            peek = self.peek()
            if peek.isdigit():
                res += self.next()
            elif peek == '.' and not used_point:
                res += self.next()
                used_point = True
            else:
                break
        return Token(TokenType.NUMBER, res, float(res), self.line)

    def get_tokens(self):
        tokens = []
        while not self.end_of_source():
            cur = self.next()

            # Skip the entire line after comments
            if cur == '#':
                self.pos = self.source.find('\n', self.pos + 1)
                self.line += 1
                continue

            # Increase line count on newline
            if cur == '\n':
                self.line += 1

            # Check for syntactical lexemes
            if cur in SYNTAX:
                tokens.append(self.lex_syntax(cur))

            # Check for string literal lexemes
            if cur == '"':
                tokens.append(self.lex_string())

            # Check for numerical literal lexemes
            if cur.isdigit():
                tokens.append(self.lex_number(cur))

            # Check for instruction lexemes

            # Check for blank space
            if cur == ' ' or cur == '\t':
                continue

        tokens.append(Token(TokenType.EOF, "", None, self.line))
        return tokens

    def next(self):
        cur = self.source[self.pos]
        self.pos += 1
        return cur

    def match(self, match: str):
        if self.end_of_source() or self.source[self.pos] != match:
            return False
        self.pos += 1
        return True

    def peek(self):
        return self.source[self.pos]

    def end_of_source(self):
        return self.pos >= 0 and self.pos >= len(self.source)
