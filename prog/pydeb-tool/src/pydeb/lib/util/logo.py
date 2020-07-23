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
from pydeb.lib.util.bcolors import bcolors
def print_logo():
    """Print project logo using ASCII."""
    logo = bcolors.OKBLUE + """
                          ____        ____       _     
                         |  _ \ _   _|  _ \  ___| |__  
                         | |_) | | | | | | |/ _ \ '_ \ 
                         |  __/| |_| | |_| |  __/ |_) |
                         |_|    \__, |____/ \___|_.__/ 
                                |___/                  
        """ + bcolors.ENDC
    print(logo)
