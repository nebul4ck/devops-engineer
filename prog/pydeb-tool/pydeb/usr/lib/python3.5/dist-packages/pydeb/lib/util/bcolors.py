#!/usr/bin/python3.5
"""
.. module:: pydeb.lib.util.bcolorts
  :platform: Unix/Linux
  :synopsis: Printer colors used by code
.. moduleauthor:: Ismael Narvaez
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com
"""
class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'