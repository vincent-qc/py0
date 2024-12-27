def error(self, line: int, message: str):
    raise RuntimeError(f"[line {line}]: {message}")
