from abc import ABC, abstractmethod
from parser.grammar.expression import Expression

from lexer.tokens import Token
from util.visitor import StatementVisitor


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor: StatementVisitor):
        pass


class ExpressionStatement(Statement):
    def __init__(self, expr: Expression):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


class Var(Statement):
    def __init__(self, name: Token, initializer: Expression):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var()
