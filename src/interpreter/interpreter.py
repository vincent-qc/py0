from parser.environment import Environment
from parser.grammar.expression import (
    Array,
    ArrayAccess,
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
from parser.grammar.functions import Callable, FunctionCallable, ReturnException
from parser.grammar.statements import (
    ExpressionStatement,
    ForStatement,
    IfStatement,
    ReturnStatement,
    Statement,
    Var,
    WhileStatement,
)
from typing import List

from interpreter.natives import define_natives
from interpreter.typecheck import checkzero, typecheck
from lexer.tokens import Token, TokenType
from util.errors import error
from util.visitor import ExpressionVisitor, StatementVisitor


class Interpreter(ExpressionVisitor, StatementVisitor):
    def __init__(self):
        self.env = Environment()
        define_natives(self.env)

    def interpret(self, statements: List[Statement]):
        for statement in statements:
            self.exec(statement)

    def visit_literal(self, literal: Literal) -> object:
        return literal.value

    def visit_grouping(self, grouping: Grouping) -> object:
        return self.eval(grouping.expr)

    def visit_unary(self, unary: Unary) -> object:
        right = self.eval(unary.right)
        if unary.op.type == TokenType.BANG:
            return not bool(right)
        elif unary.op.type == TokenType.MINUS:
            return -1 * (right)

    def visit_array(self, array: Array):
        return [self.eval(expr) for expr in array.elements]

    def visit_array_access(self, array_access: ArrayAccess):
        array = self.eval(array_access.array)
        index = self.eval(array_access.index)
        if not isinstance(array, list):
            error(array_access.bracket.line, "Array access on non-array")
        if not isinstance(index, int):
            error(array_access.bracket.line, "Array index must be an integer")
        if index < 0 or index >= len(array):
            error(array_access.bracket.line, "Array index out of bounds")
        return array[index]

    def visit_call(self, call: Call) -> object:
        callee = self.eval(call.callee)
        args = []
        for arg in call.args:
            args.append(self.eval(arg))
        if not isinstance(callee, Callable):
            error(call.paren.line, "Can only invoke functions or classes")
        func = callee
        if len(args) != func.arity():
            error(call.paren.line,
                  f"Expected {func.arity()} arguments but received {len(args)}.")
        return func.call(self, args)

    def visit_binary(self, binary: Binary) -> object:
        op = binary.op
        left = self.eval(binary.left)
        right = self.eval(binary.right)
        typecheck(op, left, right)
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
        elif op.type == TokenType.AMPERSAND:
            return left & right
        elif op.type == TokenType.PIPE:
            return left | right
        elif op.type == TokenType.XOR:
            return left ^ right
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

    def visit_logical(self, logical: Logical) -> object:
        left = bool(self.eval(logical.left))
        if logical.op.type == TokenType.OR and left:
            return True
        elif logical.op.type == TokenType.AND and not left:
            return False
        return bool(self.eval(logical.right))

    def visit_assignment(self, assignment: Assignment):
        value = self.eval(assignment.value)

        # Handle compound assignment for variables
        if isinstance(assignment.target, Token):
            if assignment.operator == TokenType.PLUS_EQUAL:
                # Get the current value
                current_value = self.env.retrive(assignment.target)
                # Add the new value
                value = current_value + value
            elif assignment.operator == TokenType.MINUS_EQUAL:
                # Get the current value
                current_value = self.env.retrive(assignment.target)
                # Subtract the new value
                value = current_value - value

            # Assign the final value
            self.env.assign(assignment.target.lexeme, value)

        # Handle compound assignment for array elements
        elif isinstance(assignment.target, ArrayAccess):
            array = self.eval(assignment.target.array)
            index = self.eval(assignment.target.index)

            if not isinstance(array, list):
                error(assignment.target.bracket.line,
                      "Cannot assign to non-array")
            if not isinstance(index, int):
                error(assignment.target.bracket.line,
                      "Array index must be an integer")
            if index < 0 or index >= len(array):
                error(assignment.target.bracket.line,
                      "Array index out of bounds")

            if assignment.operator == TokenType.PLUS_EQUAL:
                # Get the current value
                current_value = array[index]
                # Add the new value
                value = current_value + value
            elif assignment.operator == TokenType.MINUS_EQUAL:
                # Get the current value
                current_value = array[index]
                # Subtract the new value
                value = current_value - value

            array[index] = value
        else:
            error(0, "Invalid assignment target")

        return value

    def visit_variable(self, variable: Variable):
        return self.env.retrive(variable.name)

    def visit_expression_statement(self, expression_stmt: ExpressionStatement):
        return self.eval(expression_stmt.expr)

    def visit_var(self, var: Var):
        value = None
        if var.initializer is not None:
            value = self.eval(var.initializer)
        try:
            self.env.assign(var.name.lexeme, value)
        except RuntimeError:
            self.env.define(var.name.lexeme, value)

    def visit_block(self, block, new_env=None):
        new_env = Environment(self.env) if new_env is None else new_env
        old_env = self.env
        self.env = new_env
        try:
            for statement in block.statements:
                self.exec(statement)
        finally:
            self.env = old_env

    def visit_function(self, function):
        callable = FunctionCallable(function)
        self.env.define(function.name.lexeme, callable)

    def visit_if_statement(self, if_stmt: IfStatement):
        if bool(self.eval(if_stmt.condition)):
            self.exec(if_stmt.then_stmt)
        elif if_stmt.else_stmt is not None:
            self.exec(if_stmt.else_stmt)

    def visit_while_statement(self, while_stmt: WhileStatement):
        while bool(self.eval(while_stmt.condition)):
            self.exec(while_stmt.body)

    def visit_for_statement(self, for_stmt: ForStatement):
        iterator = self.eval(for_stmt.iterator)
        for item in iterator:
            env = Environment(self.env)
            env.define(for_stmt.name.lexeme, item)
            old_env = self.env
            self.env = env
            try:
                self.exec(for_stmt.body)
            finally:
                self.env = old_env

    def visit_return_statement(self, return_stmt: ReturnStatement):
        value = None
        if return_stmt.expr is not None:
            value = self.eval(return_stmt.expr)
        raise ReturnException(value)

    def eval(self, expr: Expression) -> object:
        return expr.accept(self)

    def exec(self, statement: Statement):
        return statement.accept(self)
