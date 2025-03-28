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
from parser.grammar.statements import (
    Block,
    ExpressionStatement,
    ForStatement,
    Function,
    IfStatement,
    ReturnStatement,
    Statement,
    Var,
    WhileStatement,
)
from typing import List

from lexer.tokens import SYNCHRONIZATION, Token, TokenType


class Parser():
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.index = 0

    def parse(self) -> List[Statement]:
        statements = []
        while not self.end_of_tokens():
            if not self.end_of_tokens():
                stmt = self.decleration()
                if stmt is not None:
                    statements.append(stmt)

        return statements

    def peek(self, offset=0):
        # Simple peek with bounds checking
        idx = self.index + offset
        if idx >= len(self.tokens):
            idx = len(self.tokens) - 1
        return self.tokens[idx]

    def consume(self) -> Token:
        token = self.peek()
        self.index += 1
        return token

    def match(self, *args: TokenType) -> bool:
        for arg in args:
            if self.peek().type == arg:
                return True
        return False

    def expect(self, type: TokenType, message: str) -> Token:
        if not self.match(type):
            raise RuntimeError(message + f" Instead got {self.peek().lexeme}")
        else:
            return self.consume()

    # Syntax Rules

    def decleration(self) -> Statement:
        try:
            # First check if it's a function declaration
            if self.match(TokenType.DEF):
                return self.function_decleration()

            # Then check if it's a variable declaration
            if self.match(TokenType.IDENTIFIER):
                # Only peek at the next token if we're not at the end
                if not self.end_of_tokens() and self.peek(1).type == TokenType.EQUAL:
                    return self.var_decleration()

            # Otherwise, it's a regular statement
            return self.statement()
        except RuntimeError as e:
            print(e)
            # print("SYNCHRONIZING")
            self.synchronize()
            return None  # Return None on error

    def function_decleration(self) -> Statement:
        self.consume()  # get rid of def
        name = self.expect(TokenType.IDENTIFIER, "Expect function name.")
        self.expect(TokenType.LEFT_PAREN, "Expect parenthesis.")
        args = []
        if not self.match(TokenType.RIGHT_PAREN):
            args.append(self.expect(TokenType.IDENTIFIER,
                        "Invalid parameter name."))
            while self.match(TokenType.COMMA):
                self.consume()  # consume comma
                args.append(self.expect(TokenType.IDENTIFIER,
                            "Invalid parameter name."))
        self.expect(TokenType.RIGHT_PAREN, "Expect parenthesis.")
        body = self.block()
        return Function(name, args, body)

    def var_decleration(self) -> Statement:
        name = self.consume()
        self.expect(TokenType.EQUAL, "Variable not declared.")
        initalizer = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected semicolon.")
        return Var(name, initalizer)

    def statement(self) -> Statement:
        if self.match(TokenType.LEFT_BRACE):
            return self.block()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        return self.expression_statement()

    def block(self) -> Statement:
        self.expect(TokenType.LEFT_BRACE, "Expected left brace.")
        statements = []
        while not self.end_of_tokens() and not self.match(TokenType.RIGHT_BRACE):
            statements.append(self.decleration())
        self.expect(TokenType.RIGHT_BRACE, "Unclosed brace.")
        return Block(statements)

    def if_statement(self) -> Statement:
        self.consume()  # get rid of if
        condition = self.logical_or()
        then_stmt = self.block()
        else_stmt = None
        if self.match(TokenType.ELIF):
            else_stmt = self.if_statement()
        elif self.match(TokenType.ELSE):
            self.consume()  # get rid of else
            else_stmt = self.block()
        return IfStatement(condition, then_stmt, else_stmt)

    def while_statement(self) -> Statement:
        self.consume()  # get rid of while
        condition = self.logical_or()
        body = self.block()
        return WhileStatement(condition, body)

    def for_statement(self) -> Statement:
        self.consume()  # get rid of for
        name = self.expect(TokenType.IDENTIFIER, "Expect variable name.")
        self.expect(TokenType.IN, "Expect 'in' keyword.")
        iterator = self.expression()  # iterator
        body = self.block()
        return ForStatement(name, iterator, body)

    def return_statement(self) -> Statement:
        token = self.consume()  # get rid of return
        expr = None
        if not self.match(TokenType.SEMICOLON):
            expr = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected semicolon after return.")
        return ReturnStatement(token, expr)

    def expression_statement(self) -> Statement:
        expr = self.expression()
        self.expect(TokenType.SEMICOLON, "Expected semicolon.")
        return ExpressionStatement(expr)

    def expression(self) -> Expression:
        return self.assignment()

    def assignment(self) -> Expression:
        expr = self.logical_or()
        if self.match(TokenType.EQUAL, TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL):
            op = self.consume()  # get the operator
            value = self.equality()  # a += b += 0 should not be legal

            # Check if we're assigning to a variable
            if isinstance(expr, Variable):
                name = expr.name
                return Assignment(name, value, op.type)
            # Check if we're assigning to an array element
            elif isinstance(expr, ArrayAccess):
                return Assignment(expr, value, op.type)

            raise RuntimeError("Invalid assignment target")
        return expr

    def logical_or(self) -> Expression:
        expr = self.logical_and()
        if self.match(TokenType.OR):
            op = self.consume()
            right = self.logical_and()
            expr = Logical(expr, op, right)
        return expr

    def logical_and(self) -> Expression:
        expr = self.equality()
        if self.match(TokenType.AND):
            op = self.consume()
            right = self.logical_and()
            expr = Logical(expr, op, right)
        return expr

    def equality(self) -> Expression:
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self.consume()
            right = self.comparison()
            expr = Binary(expr, op, right)
        return expr

    def comparison(self) -> Expression:
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            op = self.consume()
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def term(self) -> Expression:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS, TokenType.XOR, TokenType.AMPERSAND, TokenType.PIPE):
            op = self.consume()
            right = self.term()
            expr = Binary(expr, op, right)
        return expr

    def factor(self) -> Expression:
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH):
            op = self.consume()
            right = self.unary()
            expr = Binary(expr, op, right)
        return expr

    def unary(self) -> Expression:
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.consume()
            expr = self.unary()
            return Unary(op, expr)
        return self.array_access()

    def array_access(self) -> Expression:
        expr = self.call()
        while self.match(TokenType.LEFT_SQUARE):
            self.consume()
            index = self.expression()
            bracket = self.expect(TokenType.RIGHT_SQUARE,
                                  "Unclosed square bracket.")
            expr = ArrayAccess(expr, bracket, index)
        return expr

    def call(self) -> Expression:
        expr = self.primary()
        while self.match(TokenType.LEFT_PAREN):
            self.consume()  # get rid of left parenthesis
            args = []
            while not self.match(TokenType.RIGHT_PAREN):
                args.append(self.expression())
                if not self.match(TokenType.RIGHT_PAREN):
                    self.expect(TokenType.COMMA, "Expected comma.")
            paren = self.expect(TokenType.RIGHT_PAREN, "Unclosed parenthesis.")
            expr = Call(expr, paren, args)
        return expr

    def primary(self) -> Expression:
        if self.match(TokenType.FALSE):
            self.consume()
            return Literal(False)
        elif self.match(TokenType.TRUE):
            self.consume()
            return Literal(True)
        elif self.match(TokenType.NONE):
            self.consume()
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.consume().literal)

        if self.match(TokenType.IDENTIFIER):
            return Variable(self.consume())

        if self.match(TokenType.LEFT_PAREN):
            self.consume()  # get rid of left parenthesis
            expr = self.expression()
            self.expect(TokenType.RIGHT_PAREN, "Unclosed parenthesis.")
            return Grouping(expr)

        if self.match(TokenType.LEFT_SQUARE):
            self.consume()
            elements = []
            while not self.match(TokenType.RIGHT_SQUARE):
                elements.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.consume()
                    elements.append(self.expression())
            self.expect(TokenType.RIGHT_SQUARE, "Unclosed square bracket.")
            return Array(elements)

        raise RuntimeError(f"Expected expression. Got '{self.peek().lexeme}'.")

    def synchronize(self):
        """Synchronize after an error by advancing to the next statement."""
        while not self.end_of_tokens():
            # If we reach a semicolon, we've reached the end of the current statement
            if self.match(TokenType.SEMICOLON):
                self.consume()
                return

            # If we've reached a token that typically starts a statement, we're done
            if self.peek().type in SYNCHRONIZATION:
                return

            self.consume()

    def end_of_tokens(self) -> bool:
        return self.index >= len(self.tokens) or self.tokens[self.index].type == TokenType.EOF

    def print_ast(self, statements: List[Statement], indent: int = 0) -> None:
        """Print the AST in a readable format with proper indentation."""
        for statement in statements:
            self._print_statement(statement, indent)
