from abc import ABC, abstractmethod

from grammar.expression import Binary, Grouping, Literal, Unary


def error(self, line: int, message: str):
    raise RuntimeError(f"[line {line}]: {message}")
