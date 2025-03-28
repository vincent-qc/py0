from abc import ABC, abstractmethod
from parser.grammar.expression import Expression
from typing import Any, List, Optional

from lexer.tokens import Token


class Statement(ABC):
    @abstractmethod
    def accept(self, visitor):
        pass


class ExpressionStatement(Statement):
    def __init__(self, expr: Expression):
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_expression_statement(self)


class Var(Statement):
    def __init__(self, name: Token, initializer: Optional[Expression] = None):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visit_var(self)


class Block(Statement):
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visit_block(self, None)


class Function(Statement):
    def __init__(self, name: Token, parameters: List[Token], body: Block):
        self.name = name
        self.parameters = parameters
        self.body = body

    def accept(self, visitor):
        return visitor.visit_function(self)


class ReturnStatement(Statement):
    def __init__(self, keyword: Token, expr: Optional[Expression] = None):
        self.keyword = keyword
        self.expr = expr

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


class IfStatement(Statement):
    def __init__(self, condition: Expression, then_stmt: Statement, else_stmt: Optional[Statement] = None):
        self.condition = condition
        self.then_stmt = then_stmt
        self.else_stmt = else_stmt

    def accept(self, visitor):
        return visitor.visit_if_statement(self)


class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visit_while_statement(self)


class ForStatement(Statement):
    def __init__(self, name: Token, iterator: Expression, body: Statement):
        self.name = name
        self.iterator = iterator
        self.body = body

    def accept(self, visitor):
        return visitor.visit_for_statement(self)
