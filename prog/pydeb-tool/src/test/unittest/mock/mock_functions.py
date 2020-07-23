#!/usr/bin/python3.5
"""
.. module:: test.mock.mock_functions
  :platform: Unix/Linux
  :synopsis: Mock functions
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
def launch_cmd_mock(*args, **kwargs):
    return True

def extract_file_mock(*args, **kwargs):
    return "/tmp/test"