[![actions batch](https://github.com/luttik/auto-optional/workflows/CI/badge.svg)](
https://github.com/Luttik/auto-optional/actions?query=workflow%3ACI+branch%3Amaster
)
[![pypi](https://badge.fury.io/py/auto-optional.svg)](
https://pypi.org/project/auto-optional/
)
[![python versions](https://shields.io/pypi/pyversions/auto-optional)](
https://pypi.org/project/auto-optional/
)
[![codecov](https://codecov.io/gh/Luttik/auto-optional/branch/main/graph/badge.svg)](
https://codecov.io/gh/luttik/auto-optional
)
[![License: MIT](https://shields.io/github/license/luttik/auto-optional)](
https://github.com/Luttik/auto-optional/blob/main/LICENSE
)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# auto-optional
Makes typed arguments Optional when the default argument is None.

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
You can run this with `auto-optional [path]` (path is an optional argument).

## Properties

- Existing imports are reused.
- `import as` statements are properly handled.

## Things of note

For all these points I welcome pull-requests.

- There is no exclude (path patterns) option yet
- There is no ignore (code line) option yet
- Code is aways read and written as `UTF-8` (which is accurate most of the time).
- There is no `diff` or `check` command yet for a dry-run or linting.
