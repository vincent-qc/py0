from parser.grammar.expression import (
    Assignment,
    Binary,
    Expression,
    Grouping,
    Literal,
    Unary,
    Variable,
)
from parser.grammar.statements import ExpressionStatement, Statement, Var
from typing import List

from lexer.tokens import SYNCHRONIZATION, Token, TokenType
from util.errors import error


class Parser():
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0

    def parse(self) -> List[Statement]:
        statements = []
        while not self.end_of_tokens():
            statements.append(self.decleration())
        return statements

    def peek(self):
        return self.tokens[self.index]

    def consume(self) -> Token:
        token = self.peek()
        self.index += 1
        return token

    def match(self, *args: TokenType) -> bool:
        for arg in args:
            if self.peek().type == arg:
                return True
        return False

    def expect(self, type: TokenType, message: str) -> Token:
        if not self.match(type):
            raise RuntimeError(message)
        else:
            return self.consume()

    # Syntax Rules

    def decleration(self) -> Statement:
        try:
            # no reserved word, so proceed to variable decleration
            if self.match(TokenType.IDENTIFIER):
                return self.var_decleration()
            return self.statement()
        except RuntimeError:
            print("SYNCHRONIZING")
            self.synchronize()

    def var_decleration(self) -> Statement:
        name = self.consume()
        self.expect(TokenType.EQUAL, "Variable not declared.")
        initalizer = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected semicolon.")
        return Var(name, initalizer)

    def statement(self) -> Statement:
        return self.expression_statement()

    def expression_statement(self) -> Statement:
        expr = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected semicolon.")
        return ExpressionStatement(expr)

    def expression(self) -> Expression:
        return self.assignment()

    def assignment(self) -> Expression:
        expr = self.equality()
        if self.match(TokenType.EQUAL):
            self.consume()  # get rid of equals
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(name, value)
            raise RuntimeError("Invalid assignment target")
        return expr

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

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.consume())

        if self.match(TokenType.LEFT_PAREN):
            self.consume()  # get rid of left parenthesis
            expr = self.expression()
            self.expect(TokenType.RIGHT_PAREN, "Unclosed parenthesis.")
            return Grouping(expr)

        raise RuntimeError("Expected expression.")

    def synchronize(self):
        while not self.end_of_tokens():
            self.consume()
            if self.peek().type in SYNCHRONIZATION:
                return

    def end_of_tokens(self) -> bool:
        return self.tokens[self.index].type == TokenType.EOF
