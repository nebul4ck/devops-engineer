#!/usr/bin/python3.5
"""
.. module:: pydeb.lib.util.argparse_type
  :platform: Unix/Linux
  :synopsis: Argparse custom types
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
import argparse
import os

def readable_dir(dir):
        if not os.path.isdir(dir):
            raise argparse.ArgumentTypeError("{0} is not a valid path".format(dir))
        else:
            return dir
