from abc import ABC
from pathlib import Path
from typing import List, Union

import py
import pytest
from pydantic import BaseModel
from typer.testing import CliRunner
from yaml import load

from auto_optional.file_handling import convert_file
from auto_optional.main import app

try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import YamlLoader  # type: ignore


runner = CliRunner()


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


def prepare_file(
    test_config: Union[BeforeAndAfterTest, UnchangedTest], tmpdir: Path
) -> Path:
    if isinstance(test_config, BeforeAndAfterTest):
        code = test_config.before
    elif isinstance(test_config, UnchangedTest):
        code = test_config.unchanged
    else:
        raise NotImplementedError(
            f"tests of type {type(test_config)} are not yet supported"
        )

    code_path = tmpdir / f"{hash(code)}.py"
    code_path.write_text(code)
    return code_path


def assert_code_processed_correctly(
    test_config: Union[BeforeAndAfterTest, UnchangedTest],
    path: Path,
) -> None:
    if isinstance(test_config, BeforeAndAfterTest):
        code = test_config.after
    elif isinstance(test_config, UnchangedTest):
        code = test_config.unchanged
    else:
        raise NotImplementedError(
            f"tests of type {type(test_config)} are not yet supported"
        )

    assert path.read_text() == code


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


@pytest.mark.parametrize(
    "test_config",
    SINGLE_FILE_TESTS,
    ids=[test.name for test in SINGLE_FILE_TESTS],
)
def test_cli_single_files_from_yaml(
    test_config: Union[BeforeAndAfterTest, UnchangedTest], tmpdir: py.path.local
) -> None:
    single_code_file_path = prepare_file(test_config, Path(tmpdir))
    runner.invoke(app, [str(single_code_file_path)])
    assert_code_processed_correctly(test_config, single_code_file_path)


@pytest.mark.parametrize(
    "test_config",
    SINGLE_FILE_TESTS,
    ids=[test.name for test in SINGLE_FILE_TESTS],
)
def test_cli_no_file_should_use_current_dir(
    test_config: Union[BeforeAndAfterTest, UnchangedTest], tmpdir: py.path.local
) -> None:
    tmpdir.chdir()
    single_code_file_path = prepare_file(test_config, Path(tmpdir))
    runner.invoke(app)
    assert_code_processed_correctly(test_config, single_code_file_path)


def test_cli_multi_file(tmpdir: py.path.local) -> None:
    test_with_paths = [
        (test_config, prepare_file(test_config, Path(tmpdir)))
        for test_config in SINGLE_FILE_TESTS
    ]

    runner.invoke(app, [str(path) for _, path in test_with_paths])

    for test_config, path in test_with_paths:
        assert_code_processed_correctly(test_config, path)
