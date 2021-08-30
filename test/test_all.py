from auto_optional.convert import convert_file


def test_simple_change():
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

def test_simple_change_already_imported():
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


def test_simple_change_already_imported_optional_as():
    before = """
from typing import Optional as O
def bla(foo: str = None):
    ...
    """
    after = """
from typing import Optional as O
def bla(foo: O[str] = None):
    ...
    """
    assert convert_file(before) == after


def test_nested_change():
    before = """
def bla(foo: Tuple[str] = None):
    ...
    """
    after = """
from typing import Optional
def bla(foo: Optional[Tuple[str]] = None):
    ...
    """
    assert convert_file(before) == after

def test_not_optional():
    before = """
def bla(foo: str = 'a'):
    ...
    """
    assert convert_file(before) == before

def test_nochange():
    before = """
from typing import Optional
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == before


def test_nochange_typing_import():
    before = """
from typing import Optional
def bla(foo: Optional[str] = None):
    ...
    """
    assert convert_file(before) == before


def test_nochange_typing_as_import():
    before = """
import typing as t
def bla(foo: t.Optional[str] = None):
    ...
    """
    assert convert_file(before) == before
