from abc import ABC, abstractmethod
from parser.grammar.expression import (
    Assignment,
    Binary,
    Grouping,
    Literal,
    Unary,
    Variable,
)
from parser.grammar.statements import Block, ExpressionStatement, Var


class ExpressionVisitor(ABC):
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

    @abstractmethod
    def visit_assignment(self, assignment: Assignment):
        pass

    @abstractmethod
    def visit_variable(self, variable: Variable):
        pass


class StatementVisitor(ABC):
    @abstractmethod
    def visit_expression_statement(self, experession_stmt: ExpressionStatement):
        pass

    def visit_var(self, var: Var):
        pass

    def visit_block(self, block: Block):
        pass


class ExpressionPrinter(ExpressionVisitor):
    def visit_binary(self, binary: Binary):
        return f"({binary.left.accept(self)} {binary.op.lexeme} {binary.right.accept(self)})"

    def visit_grouping(self, grouping: Grouping):
        return f"(group {grouping.expr.accept(self)})"

    def visit_literal(self, literal: Literal):
        return str(literal.value)

    def visit_unary(self, unary: Unary):
        return f"({unary.op.lexeme} {unary.right.accept(self)})"
