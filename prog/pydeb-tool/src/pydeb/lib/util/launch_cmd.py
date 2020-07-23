#!/usr/bin/python3.5
"""
.. module:: pydeb.lib.util.launch_cmd
  :platform: Unix/Linux
  :synopsis: Cmd tools used by code
.. moduleauthor:: Isaac Pena, Ismael Narvaez
  :Nickname: ipena, inarvaez
  :mail: ipena@wtelecom.es, inarvaez@wtelecom.es
  :Web : github.com
"""

from subprocess import PIPE, Popen
from os.path import isdir

def launch_cmd(cmd: str, logger: "logger", cwd=None, env=None) -> bool:
    """Executed cmd through subprocess call.

    :param cmd: command to execute.
    :type cmd: list
    :param logger: logging instance.
    :type logger: logging.
    :param cwd: Current working directory.
    :type cwd: str
    :param env: Environment
    :type env: environ
    :return: True if successful, False otherwise
    :rtype: bool
    """
    result = None

    if not isinstance(cmd, list):
        logger.error('Command must to be a list.')
        result = False

    if not cmd:
        logger.error('Empty command detected.')
        result = False

    if result is None:
        try:
            logger.debug('Executing command: {0}'.format(str(cmd)))
            with Popen(cmd, shell=False, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env) as proc:
                for line in proc.stdout.read().decode().split("\n"):
                    if line:
                        logger.info(line)
                for line in proc.stderr.read().decode().split("\n"):
                    if line:
                        logger.info(line)
            result = True
        except Exception as e:
            logger.error('Invalid command: %s' % str(cmd))
            logger.exception(e)
            result = False
    if result is None:
        result = False
    return result