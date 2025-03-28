from typing import Optional

from lexer.tokens import Token


class Environment:
    def __init__(self, enclosing: Optional['Environment'] = None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def assign(self, name: str, value: object):
        # Fix the assignment logic to properly update variables in the current scope
        if name in self.values:
            self.values[name] = value
            return value  # Return the value to indicate success
        elif self.enclosing is not None:
            # Pass up to parent scope
            return self.enclosing.assign(name, value)
        raise RuntimeError(f"Variable {name} not defined")

    def retrive(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.retrive(name)
        raise RuntimeError(f"Variable {name.lexeme} not defined")

    def delete(self, name: Token):
        if name.lexeme in self.values:
            self.values.pop(name.lexeme)
