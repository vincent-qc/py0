from typing import List, Optional

from grammar.expression import Binary, Expression, Grouping, Literal, Unary
from tokens import SYNCHRONIZATION, Token, TokenType
from util import error


class Parser():
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0

    def parse(self) -> Optional[Expression]:
        try:
            return self.expression()
        except Exception:
            return

    def peek(self):
        return self.tokens[self.index]

    def match(self, *args: TokenType) -> bool:
        for arg in args:
            if self.peek().type == arg:
                return True
        return False

    def consume(self) -> Token:
        token = self.peek()
        self.index += 1
        return token

    def expression(self):
        return self.equality()

    def equality(self) -> Expression:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self.consume()
            right = self.comparison()
            expr = Binary(expr, op, right)
        return expr

    def comparison(self) -> Expression:
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            op = self.consume()
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def term(self) -> Expression:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.consume()
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def factor(self) -> Expression:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.consume()
            right = self.unary()
            expr = Binary(expr, op, right)
        return expr

    def unary(self) -> Expression:
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.consume()
            expr = self.unary()
            return Unary(op, expr)
        return self.primary()

    def primary(self) -> Expression:
        if self.match(TokenType.FALSE):
            self.consume()
            return Literal(False)
        elif self.match(TokenType.TRUE):
            self.consume()
            return Literal(True)
        elif self.match(TokenType.NONE):
            self.consume()
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.consume().literal)

        if self.match(TokenType.LEFT_PAREN):
            left_paren = self.consume()
            expr = self.expression()
            if not self.match(TokenType.RIGHT_PAREN):
                error(left_paren.line, "Unclosed parentheses")
            self.consume()  # get rid of right parenthesis
            return Grouping(expr)

        raise RuntimeError("Expected expression.")

    def synchronize(self):
        while not self.end_of_tokens():
            self.consume()
            if self.peek().type in SYNCHRONIZATION:
                return

    def end_of_tokens(self) -> bool:
        return self.tokens[self.index].type == TokenType.EOF
