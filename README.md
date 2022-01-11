# auto-optional
<img src="https://raw.githubusercontent.com/Luttik/auto-optional/main/docs/assets/images/logo-with-text.svg" style="width: 100%; margin: 32pt 0" alt="Logo">


<p align="center">
    auto-optional: adds the Optional type-hint to arguments where the default value is None
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

## What does auto-optional do
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

## Why would you want this

- Easily modify external libraries that didn't pay attention 
  to proper use of optional to improve mypy lintingf.
- Force consistency in your own code-base: 
  Enforcing that `None` parameter implies an `Optional` type. 
- Explicit is better than implicit — [pep 20](https://www.python.org/dev/peps/pep-0020/)

## In the media:
auto-optional was covered on 
[PythonBytes #251](https://pythonbytes.fm/episodes/show/251/a-95-complete-episode-wait-for-it)

> I love these little tools that you can run against your code that will just reformat them to be better.
>
> — Michael Kennedy

## Install
Install with `pip install auto-optional`.

## Run
After installing you can run auto-optional using `auto-optional [paths...]`
(if no path is provided it'll process the current working directory).

## pre-commit

You can run auto-optional via [pre-commit](https://pre-commit.com/).
Add the following text to your repositories `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/luttik/auto-optional
  rev: v0.3.1 # The version of auto-optional to use
  hooks:
  - id: auto-optional
```

## Things of note

### Things that are handled well

- The alternatives to `Optional` are supported, that means both;
    - `Union[X, None]`
    - `x | None` (allowed since python 3.10+).
- Existing imports are reused.
    - `import as` and `from typing import ...` statements are properly handled.

### Things that need improvement
For all these points you can leave a thumbs-up if you want it. Also, I welcome pull-requests for these issues.

- There is no exclude (for file patterns) option yet [[#2]](https://github.com/Luttik/auto-optional/issues/2)
- There is no ignore (for code lines) option yet [[#3]](https://github.com/Luttik/auto-optional/issues/3)
- Code is aways read and written as `UTF-8` (which is accurate most of the time). [[#4]](https://github.com/Luttik/auto-optional/issues/4)
- There is no `diff` or `check` command yet for a dry-run or linting. [[#5]](https://github.com/Luttik/auto-optional/issues/5)
