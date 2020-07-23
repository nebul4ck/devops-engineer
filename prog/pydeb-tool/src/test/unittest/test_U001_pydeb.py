#!/usr/bin/python3.5
"""
.. module:: test.unittest.test_U001_pydeb
  :platform: Unix/Linux
  :synopsis: Test for PyDeb main class
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
import pytest
import os
from os.path import basename
from tempfile import NamedTemporaryFile, TemporaryDirectory
from pydeb.pydeb import PyDeb
from test.unittest.mock.mock_args_parsed import ArgsParsed
from test.unittest.mock.mock_class import MockClass
from test.unittest.mock.mock_functions import extract_file_mock, launch_cmd_mock
from test.unittest.fixtures import logger_fixture

test_init_data_args = "requirements_file, pip_exec, python_exec, dest, expected"
test_001_init_data_values = [
        (NamedTemporaryFile(), "pip3", "python3", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pip2", "python2", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pip", "python", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pip4", "python", TemporaryDirectory(), False),
        ("wrong", "pip", "python", TemporaryDirectory(), False),
        (NamedTemporaryFile(), "pip3", "python3", "wrong", False),
    ]
@pytest.mark.parametrize(test_init_data_args, test_001_init_data_values)
def test_001_init_class(requirements_file, pip_exec, python_exec, dest, expected, logger_fixture):
    if hasattr(dest, 'name'):
        dest_name = dest.name
    else:
        dest_name = dest
    settings = {
        'args': ArgsParsed(requirements_file, python_exec, dest_name),
        'pip_exec': pip_exec,
        'logger': logger_fixture,
        'package_generator': MockClass,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    result = False
    try:
        pydeb_object = PyDeb(settings)
        result = bool(pydeb_object)
    except ValueError as e:
        result = False
    if hasattr(dest, 'cleanup'):
        dest.cleanup()
    assert result == expected


test_002_init_data_values = [
        (NamedTemporaryFile(), "pip3", "python3", TemporaryDirectory(), True),
        ("", "pip3", "python3", TemporaryDirectory(), False),
        (1234, "pip3", "python3", TemporaryDirectory(), False),
        ("wrong", "pip3", "python3", TemporaryDirectory(), False),
        (list(), "pip3", "python3", TemporaryDirectory(), False),
        (None, "pip3", "python3", TemporaryDirectory(), False),
        (dict(), "pip3", "python3", TemporaryDirectory(), False),
        ("........", "pip3", "python3", TemporaryDirectory(), False),
    ]
@pytest.mark.parametrize(test_init_data_args, test_002_init_data_values)
def test_002_get_requirements_file_path(requirements_file, pip_exec, python_exec, dest, expected, logger_fixture):
    if hasattr(dest, 'name'):
        dest_name = dest.name
    else:
        dest_name = dest
    settings = {
        'args': ArgsParsed(requirements_file, python_exec, dest_name),
        'pip_exec': pip_exec,
        'logger': logger_fixture,
        'package_generator': MockClass,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    result = False
    try:
        pydeb_object = PyDeb(settings)
        if pydeb_object._get_requirements_file_path() == requirements_file.name:
            result = True
    except ValueError:
        result = False
    if hasattr(dest, 'cleanup'):
        dest.cleanup()
    assert result == expected


test_003_init_data_values = [
        (NamedTemporaryFile(), "pip", "python3", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pip2", "python3", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pi", "python3", TemporaryDirectory(), False),
        (NamedTemporaryFile(), 1111, "python3", TemporaryDirectory(), False),
        (NamedTemporaryFile(), list(), "python3", TemporaryDirectory(), False),
        (NamedTemporaryFile(), None, "python3", TemporaryDirectory(), False),
    ]
@pytest.mark.parametrize(test_init_data_args, test_003_init_data_values)
def test_003_get_pip_exec(requirements_file, pip_exec, python_exec, dest, expected, logger_fixture):
    if hasattr(dest, 'name'):
        dest_name = dest.name
    else:
        dest_name = dest
    settings = {
        'args': ArgsParsed(requirements_file, python_exec, dest_name),
        'pip_exec': pip_exec,
        'logger': logger_fixture,
        'package_generator': MockClass,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    result = False
    try:
        pydeb_object = PyDeb(settings)
        if pydeb_object._get_pip_exec(pip_exec) == pip_exec:
            result = True
    except (ValueError,TypeError):
        result = False
    if hasattr(dest, 'cleanup'):
        dest.cleanup()
    assert result == expected


test_004_init_data_values = [
        (NamedTemporaryFile(), "pip", "python3", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pip2", "python3", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pi", "python3", TemporaryDirectory(), False),
        (NamedTemporaryFile(), 1111, "python3", TemporaryDirectory(), False),
        (NamedTemporaryFile(), list(), "python3", TemporaryDirectory(), False),
        (NamedTemporaryFile(), None, "python3", TemporaryDirectory(), False),
    ]
@pytest.mark.parametrize(test_init_data_args, test_004_init_data_values)
def test_004_get_python_exec(requirements_file, pip_exec, python_exec, dest, expected, logger_fixture):
    if hasattr(dest, 'name'):
        dest_name = dest.name
    else:
        dest_name = dest
    settings = {
        'args': ArgsParsed(requirements_file, python_exec, dest_name),
        'pip_exec': pip_exec,
        'logger': logger_fixture,
        'package_generator': MockClass,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    result = False
    try:
        pydeb_object = PyDeb(settings)
        if pydeb_object._get_python_exec() == python_exec:
            result = True
    except (ValueError,TypeError):
        result = False
    if hasattr(dest, 'cleanup'):
        dest.cleanup()
    assert result == expected


test_005_init_data_values = [
        (NamedTemporaryFile(), "pip", "python3", TemporaryDirectory(), True),
        (NamedTemporaryFile(), "pip", "python3", "wrong", False),
        (NamedTemporaryFile(), "pip", "python3", 1111, False),
        (NamedTemporaryFile(), "pip", "python3", None, False),
        (NamedTemporaryFile(), "pip", "python3", "", False),
    ]
@pytest.mark.parametrize(test_init_data_args, test_005_init_data_values)
def test_005_get_dest_path(requirements_file, pip_exec, python_exec, dest, expected, logger_fixture):
    if hasattr(dest, 'name'):
        dest_name = dest.name
    else:
        dest_name = dest
    settings = {
        'args': ArgsParsed(requirements_file, python_exec, dest_name),
        'pip_exec': pip_exec,
        'logger': logger_fixture,
        'package_generator': MockClass,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    result = False
    try:
        pydeb_object = PyDeb(settings)
        if pydeb_object._get_dest_path() == dest_name:
            result = True
    except (ValueError, TypeError):
        result = False
    if hasattr(dest, 'cleanup'):
        dest.cleanup()
    assert result == expected

test_006_init_data_args = "file_tmp, expected"
test_006_init_data_values = [
        (NamedTemporaryFile(), True),
        ("wrong", False),
        (list(), False),
        (dict(), False),
        (None, False),
    ]
@pytest.mark.parametrize(test_006_init_data_args, test_006_init_data_values)
def test_006_is_deb_package_createdh(file_tmp, expected, logger_fixture):
    if hasattr(file_tmp, 'name'):
        file_tmp_name = basename(file_tmp.name)
    else:
        file_tmp_name = file_tmp
    settings = {
        'args': ArgsParsed(NamedTemporaryFile(), "python3", "/tmp"),
        'pip_exec': "pip3",
        'logger': logger_fixture,
        'package_generator': MockClass,
        'launch_cmd': launch_cmd_mock,
        'extract_file': extract_file_mock
    }
    pydeb_object = PyDeb(settings)
    assert pydeb_object._is_deb_package_created({
            'unpacked_file_name': file_tmp_name
        }) == expected
