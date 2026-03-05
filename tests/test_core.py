import pytest
from calculator.core import add, subtract, multiply, divide, safe_eval

def test_add():
    assert add(2, 3) == 5

def test_subtract():
    assert subtract(10, 7) == 3

def test_multiply():
    assert multiply(4, 2.5) == 10.0

def test_divide():
    assert divide(9, 3) == 3

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

@pytest.mark.parametrize(
    "a, op, b, expected",
    [
        (3, "+", 4, 7),
        (10, "-", 2, 8),
        (6, "*", 7, 42),
        (8, "/", 2, 4),
    ],
)
def test_safe_eval(a, op, b, expected):
    assert safe_eval(a, op, b) == expected

def test_safe_eval_bad_operator():
    with pytest.raises(ValueError):
        safe_eval(1, "^", 2)