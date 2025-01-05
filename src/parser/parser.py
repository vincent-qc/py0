from parser.grammar.expression import (
    Assignment,
    Binary,
    Call,
    Expression,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from parser.grammar.statements import (
    Block,
    ExpressionStatement,
    ForStatement,
    IfStatement,
    Statement,
    Var,
    WhileStatement,
)
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
        if self.match(TokenType.LEFT_BRACE):
            return self.block()
        if self.match(TokenType.IF):
            return self.if_statement()
        return self.expression_statement()

    def block(self) -> Statement:
        self.expect(TokenType.LEFT_BRACE, "Expected left brace.")
        statements = []
        while not self.end_of_tokens() and not self.match(TokenType.RIGHT_BRACE):
            statements.append(self.decleration())
        self.expect(TokenType.RIGHT_BRACE, "Unclosed brace.")
        return Block(statements)

    def if_statement(self) -> Statement:
        self.consume()  # get rid of if
        condition = self.logical_or()
        then_stmt = self.block()
        else_stmt = None
        if self.match(TokenType.ELIF):
            else_stmt = self.if_statement()
        elif self.match(TokenType.ELSE):
            self.consume()  # get rid of else
            else_stmt = self.block()
        return IfStatement(condition, then_stmt, else_stmt)

    def while_statement(self) -> Statement:
        self.consume()  # get rid of while
        condition = self.logical_or()
        body = self.block()
        return WhileStatement(condition, body)

    def for_statement(self) -> Statement:
        self.consume  # get rid of for
        name = self.consume()
        self.expect(TokenType.IN)
        iterator = self.expression()  # iterator
        body = self.block()

        return ForStatement(name, iterator, body)

    def expression_statement(self) -> Statement:
        expr = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected semicolon.")
        return ExpressionStatement(expr)

    def expression(self) -> Expression:
        return self.assignment()

    def assignment(self) -> Expression:
        expr = self.logical_or()
        if self.match(TokenType.EQUAL):
            self.consume()  # get rid of equals
            value = self.equality()  # a = b = 0 should not be legal
            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(name, value)
            raise RuntimeError("Invalid assignment target")
        return expr

    def logical_or(self) -> Expression:
        expr = self.logical_and()
        if self.match(TokenType.OR):
            op = self.consume()
            right = self.logical_and()
            expr = Logical(expr, op, right)
        return expr

    def logical_and(self) -> Expression:
        expr = self.equality()
        if self.match(TokenType.AND):
            op = self.consume()
            right = self.logical_and()
            expr = Logical(expr, op, right)
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
        return self.call()

    def call(self) -> Expression:
        expr = self.primary()
        while self.match(TokenType.LEFT_PAREN):
            args = []
            while not self.match(TokenType.RIGHT_PAREN):
                args.append(self.expression())
                if not self.match(TokenType.RIGHT_PAREN):
                    self.expect(TokenType.COMMA, "Expected comma.")
            paren = self.expect(TokenType.RIGHT_PAREN, "Unclosed parenthesis.")
            expr = Call(expr, paren, args)
        return expr

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
