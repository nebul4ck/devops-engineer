#!/usr/bin/python3
"""
.. module:: main
  :platform: Unix/Linux
  :synopsis: Pydeb main class
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""

#import pycroncrete
import argparse
from pydeb.pydeb import PyDeb
from pydeb.lib.package_generator import PackageGenerator
from pydeb.lib.util.argparse_type import readable_dir
from pydeb.lib.util.launch_cmd import launch_cmd
from pydeb.lib.util.extract_file import extract_file
from pydeb.lib.util.bcolors import bcolors
from pydeb.lib.util.logo import print_logo
from pydeb.lib.util.profiler import Profiler
from pydeb.config.logger import logger
from pydeb.config.settings import Settings

CONFIG_FILE = '/etc/pydeb/pydeb.conf'
DEV_CONFIG_FILE = 'pydeb.conf'

def main():
    args_parser = argparse.ArgumentParser(
        description='Converts Python source distributions to Debian binary packages.'
        )
    args_parser.add_argument(
        '-r', '--requirements',
        action="store",
        type=argparse.FileType('r'),
        help="Requirements file used to download packages.",
        required=True
    )
    args_parser.add_argument(
        '-p', '--python',
        action="store",
        help="The Python interpreter used.",
        required=True
    )
    args_parser.add_argument(
        '-d', '--dest',
        action="store",
        type=readable_dir,
        help="Destination path.",
        required=True
    )
    args = args_parser.parse_args()
    settings_object = Settings(
        dict(
            config_file=CONFIG_FILE,
            dev_config_file=DEV_CONFIG_FILE,
            logger=logger
        )
    )
    project_settings = settings_object.get_project_settings()
    pydeb_settings = {
        'args': args,
        'pip_exec': project_settings["application_settings"]["pip_exec"],
        'logger': logger,
        'package_generator': PackageGenerator,
        'launch_cmd': launch_cmd,
        'extract_file': extract_file
    }
    if settings_object.is_profiler_enabled():
        profiler_settings = {
            "stats_path": project_settings["profiler_settings"]["stats_path"],
            "sort_by": project_settings["profiler_settings"]["sort_by"]
        }
        profiler_object = Profiler(profiler_settings)
        profiler_object.start()
    try:
        print_logo()
        pydeb = PyDeb(pydeb_settings)
        result = pydeb.make_packages()
        for key in result.keys():
            if result[key]:
                print(
                    key + ": " + bcolors.OKGREEN + "OK" + bcolors.ENDC
                )
            else:
                print(
                    key + ": " + bcolors.FAIL + "Fail" + bcolors.ENDC
                )
    except Exception as e:
        logger.exception(e)
    
    if settings_object.is_profiler_enabled():
        profiler_object.stop()

if __name__ == "__main__":
    main()
