class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value: object):
        self.values[name] = value

    def retrive(self, name: str) -> object:
        if name not in self.values:
            raise RuntimeError(f"Variable {name} not defined")
        return self.values[name]
