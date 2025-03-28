from abc import ABC, abstractmethod
from typing import List

from lexer.tokens import Token, TokenType


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


class Logical(Expression):
    def __init__(self, left: Expression, op: Token, right: Expression):
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visit_logical(self)


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


class Array(Expression):
    def __init__(self, elements: List[Expression]):
        self.elements = elements

    def accept(self, visitor):
        return visitor.visit_array(self)


class ArrayAccess(Expression):
    def __init__(self, array: Expression, bracket: Token, index: Expression):
        self.array = array
        self.bracket = bracket
        self.index = index

    def accept(self, visitor):
        return visitor.visit_array_access(self)


class Call(Expression):
    def __init__(self, callee: Expression, paren: Token, args: List[Expression]):
        self.callee = callee
        self.paren = paren
        self.args = args

    def accept(self, visitor):
        return visitor.visit_call(self)


class Assignment(Expression):
    def __init__(self, target, value: Expression, operator=TokenType.EQUAL):
        # target can now be either Token (for variables) or ArrayAccess (for array elements)
        self.target = target
        self.value = value
        self.operator = operator  # Store the operator type

    def accept(self, visitor):
        return visitor.visit_assignment(self)


class Variable(Expression):
    def __init__(self, name: Token):
        self.name = name

    def accept(self, visitor):
        return visitor.visit_variable(self)
