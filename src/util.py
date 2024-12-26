from abc import ABC, abstractmethod

from grammar.expression import Binary, Grouping, Literal, Unary


def error(self, line: int, message: str):
    raise RuntimeError(f"[line {line}]: {message}")


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
