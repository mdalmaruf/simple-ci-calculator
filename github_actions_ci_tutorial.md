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

✅ At this point, your repo has code and tests, **but no GitHub Actions yet**.

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

# ✅ Detailed Explanation of the `ci.yml` File (What It Does and How It Works)

Think of GitHub Actions as a **robot computer** that GitHub runs for you whenever something happens (like a push or PR).  
That robot will:
1. download your code
2. set up Python
3. install dependencies
4. run tests
5. report pass/fail back to GitHub

Below is the same YAML, explained in a “code (left) → meaning (right)” style.

> Tip: YAML spacing matters. Indentation controls structure.

## 1) Workflow name
| YAML (left) | Meaning (right) |
|---|---|
| `name: Python CI` | The display name you will see in the **Actions** tab. You can name it anything like “CI”, “Tests”, etc. |

## 2) Triggers (`on:`) — When should CI run?
| YAML (left) | Meaning (right) |
|---|---|
| ```yaml
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
``` | **Trigger events**. This workflow runs automatically when: (1) you **push** to `main`, (2) you open/update a **pull request** targeting `main`. |

**Why this matters:**  
- Push trigger protects `main` by constantly checking it.
- PR trigger ensures code is tested **before merge**.

## 3) Jobs (`jobs:`) — What work will run?
| YAML (left) | Meaning (right) |
|---|---|
| ```yaml
jobs:
  test:
    ...
``` | A workflow can have **multiple jobs** (build, test, lint, deploy). Here we define one job named `test`. |

## 4) Runner machine (`runs-on:`) — Where does it run?
| YAML (left) | Meaning (right) |
|---|---|
| `runs-on: ubuntu-latest` | GitHub starts a fresh **Ubuntu Linux VM** for this job. Every run begins clean (no leftover files). |

## 5) Matrix strategy — Run on multiple Python versions
| YAML (left) | Meaning (right) |
|---|---|
| ```yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
``` | Creates **3 parallel runs**: one per Python version. If one version fails, you will see that version’s job fail. |

## 6) Steps — The exact instructions the robot follows
Inside a job, `steps:` are executed **top to bottom**.

### Step A — Checkout code
| YAML (left) | Meaning (right) |
|---|---|
| ```yaml
- name: Checkout repository
  uses: actions/checkout@v4
``` | Downloads your repository into the runner VM. Without checkout, the runner has **no code**. |

### Step B — Install Python
| YAML (left) | Meaning (right) |
|---|---|
| ```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: ${{ matrix.python-version }}
``` | Installs Python version from the matrix. `${{ ... }}` is GitHub Actions expression syntax. |

### Step C — Install dependencies
| YAML (left) | Meaning (right) |
|---|---|
| ```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
``` | Runs shell commands: upgrades pip and installs packages from `requirements.txt` (pytest). |

### Step D — Run tests
| YAML (left) | Meaning (right) |
|---|---|
| ```yaml
- name: Run tests
  run: |
    pytest -q
``` | Executes pytest. If tests fail, the job is marked ❌ failed. If tests pass, ✅ success. |

---

## 7) Where to see results in GitHub
- Open your repository on GitHub
- Click the **Actions** tab
- Click the latest workflow run
- Open job logs to see exact commands and error messages

---

## Step 6 — Push Workflow and Watch CI Run

```bash
git add .github/workflows/ci.yml
git commit -m "Add GitHub Actions CI"
git push
```

Now open GitHub → **Actions** tab and you will see the pipeline running.

---

## Step 7 — Demonstrate CI Failure (PR demo)

1. Create a branch:
   ```bash
   git checkout -b bug-demo
   ```
2. Introduce a bug (example: in `add`, change `a + b` to `a - b`)
3. Commit + push:
   ```bash
   git add .
   git commit -m "Introduce bug for CI demo"
   git push -u origin bug-demo
   ```
4. Open a **Pull Request** from `bug-demo` → `main`

✅ CI will run automatically on the PR and fail ❌.

5. Fix the bug, push again → CI becomes green ✅.

---

## Learning Outcomes
Students will understand:
- How CI triggers run on push and pull requests
- How the YAML workflow defines jobs and steps
- How GitHub Actions installs dependencies and runs tests
- How failures appear in logs and block merges (in real projects)

---

## Optional Extensions (Next Lab)
- Add `flake8` linting (code style checks)
- Add coverage (`pytest-cov`) and print coverage percent
- Add a README badge for CI status
- Add a “deploy job” that runs only if tests pass
