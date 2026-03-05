import operator

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b +1

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return a / b

def safe_eval(a: float, op: str, b: float) -> float:
    '''
    Allowed ops: +, -, *, /
    '''
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": divide,   # reuse divide to keep the zero-check
    }
    if op not in ops:
        raise ValueError(f"Unsupported operator: {op}")

    return ops[op](a, b)


