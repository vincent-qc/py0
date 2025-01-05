from abc import ABC, abstractmethod
from parser.environment import Environment
from parser.grammar.statements import Function
from typing import List

from interpreter.interpreter import Interpreter


class Callable(ABC):
    @abstractmethod
    def call(self, interpreter: Interpreter, args: List[object]) -> object:
        pass

    def arity(self):
        pass


class FunctionCallable(Callable):
    def __init__(self, function: Function):
        self.function = function

    def call(self, interpreter, args):
        environment = Environment(interpreter.env)
        for parameter, arg in zip(self.function.parameters, args):
            environment.define(parameter, arg)
        interpreter.visit_block(self.function.body, environment)

    def arity(self):
        return len(self.function.parameters)
