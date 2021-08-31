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

## run
You can run this with `auto-optional [path]` (path is an optional argument).

## Properties

- Existing imports are reused.
- 
- `import as` statements are properly handled.

## Things of note

For all these points I welcome pull-requests.

- There is no exclude (path patterns) option yet
- There is no ignore (code line) option yet
- Code is aways read and written as `UTF-8` (which is accurate most of the time).
