from abc import ABC, abstractmethod

from lexer.tokens import Token


class Expression(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class Binary(Expression):
    def __init__(self, left: Expression, op: Token, right: Expression):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_binary(self)


class Grouping(Expression):
    def __init__(self, expr: Expression):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_grouping(self)


class Literal(Expression):
    def __init__(self, value: object):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)


class Unary(Expression):
    def __init__(self, op: Token, right: Expression):
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_unary(self)


class Variable(Expression):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable()
