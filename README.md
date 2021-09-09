<img src="https://raw.githubusercontent.com/Luttik/auto-optional/main/docs/assets/images/logo-with-text.svg" style="width: 100%; margin: 32pt 0" alt="Logo">


<p align="center">
    auto-optional: Makes typed arguments Optional when the default argument is None.
</p>

<p align="center">
    <a href="https://github.com/Luttik/auto-optional/actions?query=workflow%3ACI+branch%3Amaster">
        <img src="https://github.com/luttik/auto-optional/workflows/CI/badge.svg" alt="actions batch">
    </a>
    <a href="https://pypi.org/project/auto-optional/">
        <img src="https://badge.fury.io/py/auto-optional.svg" alt="pypi">
    </a>
    <a href="https://pypi.org/project/auto-optional/">
        <img src="https://shields.io/pypi/pyversions/auto-optional" alt="python versions">
    </a>
    <a href="https://codecov.io/gh/luttik/auto-optional">
        <img src="https://codecov.io/gh/Luttik/auto-optional/branch/main/graph/badge.svg" alt="codecov">
    </a>
    <a href="https://github.com/Luttik/auto-optional/blob/main/LICENSE">
        <img src="https://shields.io/github/license/luttik/auto-optional" alt="License: MIT">
    </a>
    <a href="https://github.com/psf/black">
        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
    </a>
</p>

---

**Documentation**: [auto-optional.daanluttik.nl](https://auto-optional.daanluttik.nl)

**Source Code**: [github.com/luttik/auto-optional](https://github.com/Luttik/auto-optional) 

---

# Purpose
The basic purpose of auto-optional is ensuring that whenever a default argument is `None` the type annotation is Optional.

For example:
```py
def foo(bar: str = None):
    ...
```

Would turn into

```py
from typing import Optional
def foo(bar: Optional[str] = None):
    ...
```

## Install
Install with `pip install auto-optional`.

## Run
After installing you can run auto-optional using `auto-optional [path]` (path is an optional argument).

## Properties

- Existing imports are reused.
- `import as` statements are properly handled.

## Things of note

For all these points I welcome pull-requests.

- There is no exclude (for file patterns) option yet
- There is no ignore (for code lines) option yet
- Code is aways read and written as `UTF-8` (which is accurate most of the time).
- There is no `diff` or `check` command yet for a dry-run or linting.
