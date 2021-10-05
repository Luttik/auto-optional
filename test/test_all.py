from abc import ABC
from pathlib import Path
from typing import List, Union

import pytest
from pydantic import BaseModel
from yaml import load

from auto_optional.file_handling import convert_file

try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import YamlLoader  # type: ignore


class BaseTestConfig(BaseModel, ABC):
    name: str


class BeforeAndAfterTest(BaseTestConfig):
    before: str
    after: str


class UnchangedTest(BaseTestConfig):
    unchanged: str


class SimpleTestConfig(BaseModel):
    tests: List[Union[BeforeAndAfterTest, UnchangedTest]]


def get_singe_file_tests() -> List:
    with (Path(__file__).parent / "simple-tests.yaml").open() as file:
        return SimpleTestConfig(
            **load(
                file,
                Loader=YamlLoader,
            )
        ).tests


SINGLE_FILE_TESTS = get_singe_file_tests()


@pytest.mark.parametrize(
    "test_config",
    SINGLE_FILE_TESTS,
    ids=[test.name for test in SINGLE_FILE_TESTS],
)
def test_single_files_from_yaml(
    test_config: Union[BeforeAndAfterTest, UnchangedTest]
) -> None:
    if isinstance(test_config, BeforeAndAfterTest):
        assert convert_file(test_config.before) == test_config.after
    elif isinstance(test_config, UnchangedTest):
        assert convert_file(test_config.unchanged) == test_config.unchanged
    else:
        raise NotImplementedError(
            f"tests of type {type(test_config)} are not yet supported"
        )
