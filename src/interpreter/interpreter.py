from parser.environment import Environment
from parser.grammar.expression import (
    Binary,
    Expression,
    Grouping,
    Literal,
    Unary,
    Variable,
)
from parser.grammar.statements import ExpressionStatement, Statement, Var
from typing import Any, List

from interpreter.typecheck import checkzero, typecheck
from lexer.tokens import Token, TokenType
from util.visitor import ExpressionVisitor, StatementVisitor


class Interpreter(ExpressionVisitor, StatementVisitor):
    def __init__(self):
        self.env = Environment()

    def interpret(self, statements: List[Statement]):
        for statement in statements:
            self.exec(statement)

    def visit_literal(self, literal: Literal) -> object:
        return literal.value

    def visit_grouping(self, grouping: Grouping) -> object:
        return self.eval(grouping)

    def visit_unary(self, unary: Unary) -> object:
        right = self.eval(unary.right)
        if unary.op.type == TokenType.BANG:
            return not bool(right)
        elif unary.op.type == TokenType.MINUS:
            return -1 * float(right)

    def visit_binary(self, binary: Binary) -> object:
        op = binary.op
        left = self.eval(binary.left)
        right = self.eval(binary.right)
        typecheck(op, right, left)
        if op.type == TokenType.PLUS:
            return left + right
        elif op.type == TokenType.MINUS:
            return left - right
        elif op.type == TokenType.STAR:
            return left * right
        elif op.type == TokenType.SLASH:
            checkzero(op, right)
            return left / right
        elif op.type == TokenType.MOD:
            checkzero(op, right)
            return left % right
        elif op.type == TokenType.GREATER:
            return left > right
        elif op.type == TokenType.GREATER_EQUAL:
            return left >= right
        elif op.type == TokenType.LESS:
            return left < right
        elif op.type == TokenType.LESS_EQUAL:
            return left <= right
        elif op.type == TokenType.EQUAL_EQUAL:
            return left == right
        elif op.type == TokenType.BANG_EQUAL:
            return left != right

    def visit_variable(self, variable: Variable):
        return self.env.retrive(variable.name.lexeme)

    def visit_expression_statement(self, expression_stmt: ExpressionStatement):
        self.exec(expression_stmt)

    def visit_var(self, var: Var):
        value = self.eval(var.initializer)
        self.env.define(var.name.lexeme, value)

    def eval(self, expr: Expression) -> object:
        return expr.accept(self)

    def exec(self, statement: Statement):
        return statement.accept(self)
