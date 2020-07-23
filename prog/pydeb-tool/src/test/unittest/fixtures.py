#!/usr/bin/python3.5
"""
.. module:: test.unittest.fixtures.fixtures
  :platform: Unix/Linux
  :synopsis: Test for PyDeb main class
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
import pytest
import logging

@pytest.fixture(scope='session')
def logger_fixture(*args, **kwargs):
    FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
    logging.basicConfig(format=FORMAT)
    return logging.getLogger()