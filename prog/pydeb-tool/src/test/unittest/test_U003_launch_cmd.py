#!/usr/bin/python3.5
"""
.. module:: test.unittest.test_U003_launch_cmd
  :platform: Unix/Linux
  :synopsis: Test for launch_cmd function
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
import pytest
import hypothesis.strategies as st
from hypothesis import given, settings
from unittest import mock
from pydeb.lib.util.launch_cmd import launch_cmd
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
@given(cmd=fake_value, cwd=fake_value, env=fake_value)
def test_001_launch_cmd_types(cmd, cwd, env, logger_fixture):
    m = mock.mock_open()
    with mock.patch('pydeb.lib.util.launch_cmd.Popen', m):
        result = launch_cmd(cmd, logger_fixture, cwd=cwd, env=env)
        assert result or not result


@settings(max_examples=NUM_EXAMPLES_HYPOTHESIS)
@given(cmd=st.lists(st.text()), cwd=st.text(), env=st.text())
def test_002_launch_cmd_text(cmd, cwd, env, logger_fixture):
    m = mock.mock_open()
    m.stdout = mock.MagicMock()
    m.stderr = mock.MagicMock()
    with mock.patch('pydeb.lib.util.launch_cmd.Popen', m):
        result = launch_cmd(cmd, logger_fixture, cwd=cwd, env=env)
        if cmd:
            assert mock.call(cmd, cwd=cwd, env=env, shell=False, stderr=-1, stdout=-1) == m.mock_calls[0]
        else:
            assert result == False