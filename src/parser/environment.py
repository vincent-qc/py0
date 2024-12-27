from lexer.tokens import Token


class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: Token, value: object):
        self.values[name.lexeme] = value

    def assign(self, name: Token, value: object):
        if name.lexeme not in self.values:
            raise RuntimeError(f"Variable {name.lexeme} not defined")
        self.values[name.lexeme] = value

    def retrive(self, name: Token) -> object:
        if name.lexeme not in self.values:
            raise RuntimeError(f"Variable {name.lexeme} not defined")
        return self.values[name.lexeme]
