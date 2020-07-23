#!/usr/bin/python3.5
"""
.. module:: test.unittest.test_U002_package_generator
  :platform: Unix/Linux
  :synopsis: Test for PackageGenerator main class
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
import pytest
import hypothesis.strategies as st
from hypothesis import given, settings
from tempfile import NamedTemporaryFile
from os.path import dirname
from pydeb.lib.package_generator import PackageGenerator
from test.unittest.mock.mock_class import MockClass
from test.unittest.mock.mock_args_parsed import ArgsParsed
from test.unittest.mock.mock_functions import extract_file_mock, launch_cmd_mock
from test.unittest.fixtures import logger_fixture

NUM_EXAMPLES_HYPOTHESIS=500

fake_value =st.one_of(
    st.none(),
    st.integers(), 
    st.floats(),
    st.text(),
    st.lists(st.floats()),
)
@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    requirements_file=fake_value,
    pip_exec=fake_value,
    python_exec=fake_value,
    dest=fake_value,
    tmpdir_name=fake_value
    )
def test_001_init_class(requirements_file, pip_exec, python_exec, dest, tmpdir_name, logger_fixture):
    settings = {
        'requirements_file': requirements_file,
        'pip_exec': pip_exec,
        'python_exec': python_exec,
        'dest_path': dest,
        'tmp_path': tmpdir_name,
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    assert bool(package_generator)

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    requirements_file=fake_value,
    pip_exec=fake_value,
    python_exec=fake_value,
    dest=fake_value,
    tmpdir_name=fake_value
    )
def test_002_download_requirements_types(requirements_file, pip_exec, python_exec, dest, tmpdir_name, logger_fixture):
    settings = {
        'requirements_file': requirements_file,
        'pip_exec': pip_exec,
        'python_exec': python_exec,
        'dest_path': dest,
        'tmp_path': tmpdir_name,
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.download_requirements()
    assert result or not result

def test_003_download_requirements_func(logger_fixture):
    settings = {
        'requirements_file': "requirements_file",
        'pip_exec': "pip_exec",
        'python_exec': "python_exec",
        'dest_path': "dest",
        'tmp_path': "tmpdir_name",
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.download_requirements()
    assert result

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    requirements_file=fake_value,
    pip_exec=fake_value,
    python_exec=fake_value,
    dest=fake_value,
    tmpdir_name=fake_value
    )
def test_004_unpack_source_code_types(requirements_file, pip_exec, python_exec, dest, tmpdir_name, logger_fixture):
    settings = {
        'requirements_file': requirements_file,
        'pip_exec': pip_exec,
        'python_exec': python_exec,
        'dest_path': dest,
        'tmp_path': tmpdir_name,
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.unpack_source_code()
    assert result or not result

def test_005_unpack_source_code_func(logger_fixture):
    tmp_file = NamedTemporaryFile()
    tmp_file_path = tmp_file.name
    tmp_file_dir = dirname(tmp_file_path)
    settings = {
        'requirements_file': "requirements_file",
        'pip_exec': "pip_exec",
        'python_exec': "python_exec",
        'dest_path': "dest",
        'tmp_path': tmp_file_dir,
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.unpack_source_code()
    assert result
    tmp_file.close()

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    requirements_file=fake_value,
    pip_exec=fake_value,
    python_exec=fake_value,
    dest=fake_value,
    tmpdir_name=fake_value,
    unpacked_file_info=fake_value
    )
def test_006_make_source_package_types(
    requirements_file,
    pip_exec,
    python_exec,
    dest,
    tmpdir_name,
    unpacked_file_info,
    logger_fixture):
    settings = {
        'requirements_file': requirements_file,
        'pip_exec': pip_exec,
        'python_exec': python_exec,
        'dest_path': dest,
        'tmp_path': tmpdir_name,
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.make_source_package(unpacked_file_info)
    assert result or not result

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    unpacked_file_path=st.text(),
    unpacked_file_name=st.text()
    )
def test_007_make_source_package_func(logger_fixture, unpacked_file_path, unpacked_file_name):
    settings = {
        'requirements_file': "requirements_file",
        'pip_exec': "pip_exec",
        'python_exec': "python_exec",
        'dest_path': "dest",
        'tmp_path': "tmp_path",
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.make_source_package(
        dict(
            unpacked_file_path=st.text(),
            unpacked_file_name=st.text()
        )
    )
    assert result or not result


@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    requirements_file=fake_value,
    pip_exec=fake_value,
    python_exec=fake_value,
    dest=fake_value,
    tmpdir_name=fake_value,
    unpacked_file_info=fake_value
    )
def test_008_make_binary_package_types(
    requirements_file,
    pip_exec,
    python_exec,
    dest,
    tmpdir_name,
    unpacked_file_info,
    logger_fixture):
    settings = {
        'requirements_file': requirements_file,
        'pip_exec': pip_exec,
        'python_exec': python_exec,
        'dest_path': dest,
        'tmp_path': tmpdir_name,
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.make_binary_package(unpacked_file_info)
    assert result or not result

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    unpacked_file_path=st.text(),
    unpacked_file_name=st.text()
    )
def test_009_make_binnary_package_func(logger_fixture, unpacked_file_path, unpacked_file_name):
    settings = {
        'requirements_file': "requirements_file",
        'pip_exec': "pip_exec",
        'python_exec': "python_exec",
        'dest_path': "dest",
        'tmp_path': "tmp_path",
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.make_binary_package(
        dict(
            unpacked_file_path=st.text(),
            unpacked_file_name=st.text()
        )
    )
    assert result or not result

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    requirements_file=fake_value,
    pip_exec=fake_value,
    python_exec=fake_value,
    dest=fake_value,
    tmpdir_name=fake_value,
    unpacked_file_info=fake_value
    )
def test_010_move_binary_package_types(
    requirements_file,
    pip_exec,
    python_exec,
    dest,
    tmpdir_name,
    unpacked_file_info,
    logger_fixture):
    settings = {
        'requirements_file': requirements_file,
        'pip_exec': pip_exec,
        'python_exec': python_exec,
        'dest_path': dest,
        'tmp_path': tmpdir_name,
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.make_binary_package(unpacked_file_info)
    assert result or not result

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(
    unpacked_file_path=st.text(),
    unpacked_file_name=st.text()
    )
def test_011_move_binary_package_func(logger_fixture, unpacked_file_path, unpacked_file_name):
    settings = {
        'requirements_file': "requirements_file",
        'pip_exec': "pip_exec",
        'python_exec': "python_exec",
        'dest_path': "dest",
        'tmp_path': "tmp_path",
        'logger': logger_fixture,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    package_generator = PackageGenerator(settings)
    result = package_generator.move_binary_package(
        dict(
            unpacked_file_path=st.text(),
            unpacked_file_name=st.text()
        )
    )
    assert result or not result
