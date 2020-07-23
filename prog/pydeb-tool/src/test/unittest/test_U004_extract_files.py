#!/usr/bin/python3.5
"""
.. module:: test.unittest.test_U004_extract_files
  :platform: Unix/Linux
  :synopsis: Test for extract_files function
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
import pytest
import hypothesis.strategies as st
from hypothesis import given, settings
from unittest import mock
from pydeb.lib.util.extract_file import extract_file
from test.unittest.fixtures import logger_fixture

NUM_EXAMPLES_HYPOTHESIS=500

fake_value =st.one_of(
    st.none(),
    st.integers(), 
    st.floats(),
    st.lists(st.floats()),
)
@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(filename=fake_value, dest_path=fake_value)
def test_001_launch_cmd_types(filename, dest_path, logger_fixture):
    settings = {
        'filename': filename,
        'dest_path': dest_path,
        'logger': logger_fixture
    }
    m_tarfile = mock.MagicMock()
    m_zipfile = mock.MagicMock()
    with mock.patch('pydeb.lib.util.extract_file.tarfile', m_tarfile):
        with mock.patch('pydeb.lib.util.extract_file.ZipFile', m_zipfile):
            result = extract_file(settings)
            assert result == False

@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(filename=st.text(), dest_path=st.text())
def test_002_launch_cmd_func(filename, dest_path, logger_fixture):
    settings_targz = {
        'filename': filename + '.tar.gz',
        'dest_path': dest_path,
        'logger': logger_fixture
    }
    settings_tar = {
        'filename': filename + '.tar',
        'dest_path': dest_path,
        'logger': logger_fixture
    }
    settings_tarbz2 = {
        'filename': filename + '.tar.bz2',
        'dest_path': dest_path,
        'logger': logger_fixture
    }
    settings_zip = {
        'filename': filename + '.zip',
        'dest_path': dest_path,
        'logger': logger_fixture
    }
    settings_wrong = {
        'filename': filename,
        'dest_path': dest_path,
        'logger': logger_fixture
    }

    mock_tarfile = mock.MagicMock()
    with mock.patch('pydeb.lib.util.extract_file.tarfile', mock_tarfile):
        result = extract_file(settings_targz)
        assert (result == filename or result == False)
        tarfile_calls = mock_tarfile.mock_calls
        tarfile_calls.pop(3)
        assert [mock.call.open(settings_targz['filename'], 'r:gz'),
                mock.call.open().__enter__(),
                mock.call.open().__enter__().getnames(),
                mock.call.open().__exit__(None, None, None),
                mock.call.open(settings_targz['filename'], 'r:gz'),
                mock.call.open().__enter__(),
                mock.call.open().__enter__().extractall(path=settings_targz['dest_path']),
                mock.call.open().__exit__(None, None, None)
                ] == tarfile_calls

    mock_tarfile = mock.MagicMock()
    with mock.patch('pydeb.lib.util.extract_file.tarfile', mock_tarfile):
        result = extract_file(settings_tar)
        assert (result == filename or result == False)
        tarfile_calls = mock_tarfile.mock_calls
        tarfile_calls.pop(3)
        assert [mock.call.open(settings_tar['filename'], 'r:'),
                mock.call.open().__enter__(),
                mock.call.open().__enter__().getnames(),
                mock.call.open().__exit__(None, None, None),
                mock.call.open(settings_tar['filename'], 'r:'),
                mock.call.open().__enter__(),
                mock.call.open().__enter__().extractall(path=settings_tar['dest_path']),
                mock.call.open().__exit__(None, None, None)
                ] == tarfile_calls


    mock_tarfile = mock.MagicMock()
    with mock.patch('pydeb.lib.util.extract_file.tarfile', mock_tarfile):
        result = extract_file(settings_tarbz2)
        assert (result == filename or result == False)
        tarfile_calls = mock_tarfile.mock_calls
        tarfile_calls.pop(3)
        assert [mock.call.open(settings_tarbz2['filename'], 'r:bz2'),
                mock.call.open().__enter__(),
                mock.call.open().__enter__().getnames(),
                mock.call.open().__exit__(None, None, None),
                mock.call.open(settings_tarbz2['filename'], 'r:bz2'),
                mock.call.open().__enter__(),
                mock.call.open().__enter__().extractall(path=settings_tarbz2['dest_path']),
                mock.call.open().__exit__(None, None, None)
                ] == tarfile_calls

    mock_zipfile = mock.MagicMock()
    with mock.patch('pydeb.lib.util.extract_file.ZipFile', mock_zipfile):
        result = extract_file(settings_zip)
        assert (result == filename or result == False)
        zipfile_calls = mock_zipfile.mock_calls
        zipfile_calls.pop(3)
        assert [
            mock.call(settings_zip['filename']),
            mock.call().__enter__(),
            mock.call().__enter__().infolist(),
            mock.call().__exit__(None, None, None)
        ] == zipfile_calls

    result = extract_file(settings_wrong)
    assert result == False