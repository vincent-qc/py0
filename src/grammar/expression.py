from abc import ABC, abstractmethod

from tokens import Token


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


class Visitor(ABC):
    @abstractmethod
    def visit_binary(self, binary: Binary):
        pass

    @abstractmethod
    def visit_grouping(self, grouping: Grouping):
        pass

    @abstractmethod
    def visit_literal(self, literal: Literal):
        pass

    @abstractmethod
    def visit_unary(self, unary: Unary):
        pass


class ExpressionPrinter(Visitor):
    def visit_binary(self, binary: Binary):
        return f"({binary.left.accept(self)} {binary.op.lexeme} {binary.right.accept(self)})"

    def visit_grouping(self, grouping: Grouping):
        return f"(group {grouping.expr.accept(self)})"

    def visit_literal(self, literal: Literal):
        return str(literal.value)

    def visit_unary(self, unary: Unary):
        return f"({unary.op.lexeme} {unary.right.accept(self)})"
