# GitHub Actions CI/CD Tutorial (Calculator Example) — With Detailed Workflow Explanation

This tutorial demonstrates how to build a simple **Python calculator project**, add **pytest unit tests**, and configure **GitHub Actions** to run **Continuous Integration (CI)** automatically on every push and pull request.

Students will:
1. Create a repository
2. Add calculator code
3. Add test cases
4. Push to GitHub
5. Add a GitHub Actions workflow (`ci.yml`)
6. See tests run automatically in the GitHub **Actions** tab
7. Break something on a branch and watch CI fail on a Pull Request

---

## Repository Structure

```
simple-ci-calculator/
├─ calculator/
│  ├─ __init__.py
│  └─ core.py
├─ tests/
│  └─ test_core.py
├─ requirements.txt
├─ README.md
└─ .github/
   └─ workflows/
      └─ ci.yml
```

---

## Step 1 — Create the Calculator Code

Create folder `calculator/` and add:

### `calculator/__init__.py`
```python
__all__ = ["add", "subtract", "multiply", "divide", "safe_eval"]
from .core import add, subtract, multiply, divide, safe_eval
```

### `calculator/core.py`
```python
import operator

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

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
```

---

## Step 2 — Add Unit Tests (pytest)

Create folder `tests/` and add:

### `tests/test_core.py`
```python
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
```

---

## Step 3 — Dependencies

### `requirements.txt`
```txt
pytest
```

Run locally (students must do this before CI):

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

---

## Step 4 — Create Repo & Push to GitHub

1. Create a new repository on GitHub named: `simple-ci-calculator`
2. Clone it:
   ```bash
   git clone <YOUR_REPO_URL>
   cd simple-ci-calculator
   ```
3. Add the files above.
4. Commit + push:
   ```bash
   git add .
   git commit -m "Add calculator + tests"
   git push origin main
   ```

At this point, your repo has code and tests, **but no GitHub Actions yet**.

---

## Step 5 — Add GitHub Actions Workflow

Create folder:
```
.github/workflows/
```

Create file:
### `.github/workflows/ci.yml`
```yaml
name: Python CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest -q
```

---

# Detailed Explanation of the `ci.yml` File (What It Does and How It Works)

Think of GitHub Actions as a **robot computer** that GitHub runs for you whenever something happens (like a push or PR).  
That robot will:
1. download your code
2. set up Python
3. install dependencies
4. run tests
5. report pass/fail back to GitHub

Below is the same YAML, explained in a “code (left) → meaning (right)” style.

> Tip: YAML spacing matters. Indentation controls structure.

# How the YAML File Works

## Workflow Name

```
name: Python CI
```

This is the name shown inside the GitHub Actions dashboard.

---

## Trigger Section

```
on:
  push:
    branches: ["main"]

  pull_request:
    branches: ["main"]
```

This tells GitHub when the pipeline should run.

The workflow starts automatically when:

• code is pushed to the main branch
• a pull request is opened to the main branch

---

## Jobs Section

```
jobs:
  test:
```

A workflow can contain multiple jobs.

Example:

* build
* test
* deploy

Here we only define one job called **test**.

---

## Runner Machine

```
runs-on: ubuntu-latest
```

GitHub launches a fresh Linux virtual machine to run the pipeline.

This ensures:

• reproducible builds
• clean environment
• no dependency conflicts

---

## Matrix Strategy

```
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

This allows testing the code with multiple Python versions.

GitHub will automatically run **three parallel jobs**.

Example:

Job 1 → Python 3.10
Job 2 → Python 3.11
Job 3 → Python 3.12

If any job fails, CI fails.

---

## Steps Section

Steps define the commands executed sequentially.

### Step 1: Checkout repository

```
uses: actions/checkout@v4
```

This downloads your repository into the runner machine.

Without this step, the CI machine would not have your code.

---

### Step 2: Install Python

```
uses: actions/setup-python@v5
```

This installs Python on the CI machine.

The version is selected from the matrix.

---

### Step 3: Install Dependencies

```
pip install -r requirements.txt
```

This installs all packages required for the project.

---

### Step 4: Run Tests

```
pytest -q
```

This executes all test cases.

If any test fails:

CI status → ❌ Failed

If all tests pass:

CI status → ✅ Success

---

# 9. Push Workflow to GitHub

```
git add .github/workflows/ci.yml

git commit -m "add github actions workflow"

git push
```

---

# 10. View CI Results

Open repository on GitHub.

Click:

```
Actions
```

You will see the CI pipeline running automatically.

---

# 11. Demonstrate CI Failure

Create a new branch.

```
git checkout -b bug-demo
```

Break the code intentionally.

Example:

```
return a + b
```

change to

```
return a - b
```

Push the branch and open a Pull Request.

CI will fail.

Fix the bug → push again → CI becomes green.

---

# Learning Outcomes

Students learn:

• Git workflow
• automated testing
• GitHub Actions pipeline
• continuous integration
• pull request validation

---

# Extension Exercises

1. Add power(a,b) function
2. Add test coverage
3. Add flake8 code linting
4. Add Docker build step
5. Add deployment pipeline
