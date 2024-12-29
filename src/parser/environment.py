from typing import Optional

from lexer.tokens import Token


class Environment:
    def __init__(self, enclosing: Optional['Environment'] = None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name: Token, value: object):
        self.values[name.lexeme] = value

    def assign(self, name: Token, value: object):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        if self.enclosing is not None:
            return self.enclosing.assign(name, value)
        raise RuntimeError(f"Variable {name.lexeme} not defined")

    def retrive(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.retrive(name)
        raise RuntimeError(f"Variable {name.lexeme} not defined")

    def delete(self, name: Token):
        if name.lexeme in self.values:
            self.values.pop(name.lexeme)
