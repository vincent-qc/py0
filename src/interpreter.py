from typing import Any, List

from grammar.expression import Expression
from tokens import TokenType
from util import Visitor


def typecheck_number(*args: object):
    for arg in args:
        if not isinstance(arg, float) and not isinstance(arg, int):
            return False
    return True


def typecheck_str(*args: object):
    for arg in args:
        if not isinstance(arg, str):
            return False
    return True


class Interpreter(Visitor):
    def interpret(self, expr):
        try:
            res = self.eval(expr)
            print("RES:", res)
        except RuntimeError:
            return

    def visit_literal(self, literal) -> object:
        return literal.value

    def visit_grouping(self, grouping) -> object:
        return self.eval(grouping)

    def visit_unary(self, unary) -> object:
        right = self.eval(unary.right)
        if unary.op.type == TokenType.BANG:
            return not bool(right)
        elif unary.op.type == TokenType.MINUS:
            return -1 * float(right)

    def visit_binary(self, binary):
        left = self.eval(binary.left)
        right = self.eval(binary.right)
        if binary.op.type == TokenType.PLUS:
            if not typecheck_number(left, right) and not typecheck_str(left, right):
                raise RuntimeError("Invalid types")
            return left + right
        elif binary.op.type == TokenType.MINUS:
            if not typecheck_number(left, right):
                raise RuntimeError("Type must be number")
            return left - right
        elif binary.op.type == TokenType.STAR:
            if not typecheck_number(left, right):
                raise RuntimeError("Type must be number")
            return left * right
        elif binary.op.type == TokenType.SLASH:
            if not typecheck_number(left, right):
                raise RuntimeError("Type must be number")
            if right == 0:
                raise RuntimeError("Cannot divide by zero")
            return left / right
        elif binary.op.type == TokenType.GREATER:
            if not typecheck_number(left, right):
                raise RuntimeError("Type must be number")
            return left > right
        elif binary.op.type == TokenType.GREATER_EQUAL:
            if not typecheck_number(left, right):
                raise RuntimeError("Type must be number")
            return left >= right
        elif binary.op.type == TokenType.LESS:
            if not typecheck_number(left, right):
                raise RuntimeError("Type must be number")
            return left < right
        elif binary.op.type == TokenType.LESS_EQUAL:
            if not typecheck_number(left, right):
                raise RuntimeError("Type must be number")
            return left <= right
        elif binary.op.type == TokenType.EQUAL_EQUAL:
            return left == right
        elif binary.op.type == TokenType.BANG_EQUAL:
            return left != right

    def eval(self, expr: Expression):
        return expr.accept(self)
