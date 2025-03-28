def error(line: int, message: str):
    raise RuntimeError(f"[line {line}]: {message}")
