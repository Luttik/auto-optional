from auto_optional.convert import convert_file


def test_simple_change() -> None:
    before = """
def bla(foo: str = None):
    ...
    """
    after = """
from typing import Optional
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == after


def test_simple_change_already_imported() -> None:
    before = """
from typing import Optional
def bla(foo: str = None):
    ...
    """
    after = """
from typing import Optional
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == after


def test_simple_change_star_import() -> None:
    before = """
from typing import *
def bla(foo: str = None):
    ...
    """
    after = """
from typing import *
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == after


def test_simple_change_already_imported_optional_as() -> None:
    before = """\
from typing import Optional as O
def bla(foo: str = None):
    ...
    """
    after = """\
from typing import Optional as O
def bla(foo: O[str] = None):
    ...
    """
    assert convert_file(before) == after


def test_nested_change() -> None:
    before = """\
def bla(foo: Tuple[str] = None):
    ...
    """
    after = """\
from typing import Optional
def bla(foo: Optional[Tuple[str]] = None):
    ...
    """
    assert convert_file(before) == after


def test_not_optional() -> None:
    before = """\
def bla(foo: str = 'a'):
    ...
    """
    assert convert_file(before) == before


def test_nochange() -> None:
    before = """\
from typing import Optional
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == before


def test_legal_no_type() -> None:
    before = """
class Bloep:
    def bla(self):
        ...
    """
    assert convert_file(before) == before


def test_nochange_typing_import() -> None:
    before = """
from typing import Optional
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == before


def test_nochange_renamed_typing() -> None:
    before = """\
import typing
import typing as t
def bla(foo: t.Optional[str] = None):
    ...
    """
    assert convert_file(before) == before


def test_prioritise_from_import() -> None:
    before = """\
import typing
from typing import Optional
def bla(foo: str = None):
    ...
    """
    after = """\
import typing
from typing import Optional
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == after


def test_nochange_typing_as_import() -> None:
    before = """\
import typing as t
def bla(foo: t.Optional[str] = None):
    ...
    """
    assert convert_file(before) == before
