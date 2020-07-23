#!/usr/bin/python3.5
"""
.. module:: test.mock.mock_args_parsed
  :platform: Unix/Linux
  :synopsis: Mock input args
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
from collections import namedtuple

ArgsParsed = namedtuple(
    'ArgsParsed', ['requirements', 'python', 'dest']
)