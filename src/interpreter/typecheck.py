

from lexer.tokens import Token, TokenType

NUMBERS = [TokenType.MINUS, TokenType.STAR, TokenType.SLASH]
BOTH = [TokenType.PLUS, TokenType.GREATER,
        TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]


def typecheck_number(*args: object):
    for arg in args:
        if not (isinstance(arg, float) or isinstance(arg, int)) and not isinstance(arg, int):
            return False
    return True


def typecheck_str(*args: object):
    for arg in args:
        if not isinstance(arg, str):
            return False
    return True


def typecheck(op: Token, left: object, right: object):
    if op in BOTH:
        if not typecheck_number(left, right) and not typecheck_str(left, right):
            raise TypeError("values must be either numbers or strings")
    elif op in NUMBERS:
        if not typecheck_number(left, right):
            raise TypeError("values must be numbers")


def checkzero(op: Token, right: object):
    if right == 0:
        raise RuntimeError(
            f"Cannot {"divide" if op.type == TokenType.SLASH else "mod"} by zero")
