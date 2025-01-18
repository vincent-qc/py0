from parser.environment import Environment
from parser.grammar.expression import (
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
from lexer.tokens import TokenType
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
        return self.eval(grouping)

    def visit_unary(self, unary: Unary) -> object:
        right = self.eval(unary.right)
        if unary.op.type == TokenType.BANG:
            return not bool(right)
        elif unary.op.type == TokenType.MINUS:
            return -1 * float(right)

    def visit_call(self, call: Call) -> object:
        callee = self.eval(call.callee)
        args = []
        for arg in call.args:
            args.append(self.eval(arg))
        if not isinstance(Callable, callee):
            error(call.paren.line, "Can only invoke functions or classes")
        func = Callable(callee)
        if len(args) != func.arity():
            error(call.paren.line,
                  f"Expected {func.arity()} arguments but received {len(args)}.")
        return func.call(self, args)

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

    def visit_logical(self, logical: Logical) -> object:
        left = bool(self.eval(logical.left))
        if logical.op.type == TokenType.OR and left:
            return True
        elif logical.op.type == TokenType.AND and not left:
            return False
        return bool(self.eval(logical.right))

    def visit_assignment(self, assignment: Assignment):
        value = self.eval(assignment.value)
        self.env.assign(assignment.name, value)

    def visit_variable(self, variable: Variable):
        return self.env.retrive(variable.name)

    def visit_expression_statement(self, expression_stmt: ExpressionStatement):
        self.exec(expression_stmt)

    def visit_var(self, var: Var):
        value = self.eval(var.initializer)
        self.env.define(var.name, value)

    def visit_block(self, block, new_env=None):
        new_env = Environment(self.env) if new_env is None else new_env
        old_env = self.env
        self.env = new_env
        for statement in block.statements:
            self.exec(statement)
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
        while while_stmt.condition:
            self.exec(while_stmt.body)

    def visit_for_statement(self, for_stmt: ForStatement):
        name = for_stmt.name
        iterator = self.eval(for_stmt.iterator)
        for item in iterator:
            self.env.define(name, item)
            self.exec(for_stmt.body)
        self.env.delete(name)

    def visit_return_statement(self, return_stmt: ReturnStatement):
        value = self.eval(return_stmt.expr)
        raise ReturnException(value)

    def eval(self, expr: Expression) -> object:
        return expr.accept(self)

    def exec(self, statement: Statement):
        return statement.accept(self)
