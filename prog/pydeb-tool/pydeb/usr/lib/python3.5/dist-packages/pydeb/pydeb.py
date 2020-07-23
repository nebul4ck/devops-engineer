#!/usr/bin/python3.5
"""
.. module:: pydeb.pydeb
  :platform: Unix/Linux
  :synopsis: PyDeb main class
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
from fnmatch import fnmatch
from re import search
from shutil import which
from tempfile import TemporaryDirectory
from os import listdir
from os.path import abspath, isfile, isdir

class PyDeb(object):
    """ Class used to generate debian packages using Pypy packages."""

    def __init__(self, settings: dict) -> None:
        """Class constructor..

        settings = {
            'args': args,
            'pip_exec': 'pip_exec_name',
            'logger': logger,
            'package_generator': PackageGenerator,
            'launch_cmd': launch_cmd,
            'extract_file': extract_file
        }
        :param settings: Class dependencies
        :type settings: dict
        """
        self.args = settings['args']
        self.logger = settings['logger']
        self.package_generator = settings['package_generator']
        self.launch_cmd = settings['launch_cmd']
        self.extract_file = settings['extract_file']
        self.requirements_file_path = self._get_requirements_file_path()
        self.python_exec = self._get_python_exec()
        self.pip_exec = self._get_pip_exec(settings['pip_exec'])
        self.dest_path = self._get_dest_path()
        self.unpacked_files = []
        self.logger.debug("Instantiated class %s" % (self.__class__.__name__))

    def _get_requirements_file_path(self) -> str:
        """Get location of requirements file.

        :return: Path
        :rtype: str
        """
        if hasattr(self.args.requirements, 'name'):
            file_name = self.args.requirements.name
            self.args.requirements.close()
            return file_name
        raise ValueError("Wrong requirements file.")

    def _get_pip_exec(self, pip_exec_name: str) -> str:
        """Get pip executable name.

        :param pip_exec_name: Pip executable name
        :type pip_exec_name: str
        :return: Name
        :rtype: str
        """
        if isinstance(pip_exec_name, str):
            scan_executable_name = search('pip[2-3]?', pip_exec_name)
            if scan_executable_name:
                if which(pip_exec_name):
                    return pip_exec_name
        raise ValueError("Wrong pip executable (pip/pip2/pip3). Install it or change conf.")

    def _get_python_exec(self) -> str:
        """Get location of python executable.

        :return: Name
        :rtype: str
        """
        if isinstance(self.args.python, str):
            scan_executable_name = search('python[2-3]?', self.args.python)
            if scan_executable_name:
                if which(self.args.python):
                    return self.args.python
        raise ValueError("Wrong python executable. Use python/python2/python3")

    def _get_dest_path(self) -> str:
        """Get dest path used to save packages.

        :return: Path
        :rtype: str
        """
        if isdir(self.args.dest) and isinstance(self.args.dest, str):
            return abspath(self.args.dest)
        raise ValueError("Wrong destination path.")

    def _is_deb_package_created(self, unpacked_file_info: dict) -> bool:
        """
        Check deb package creation.

        unpacked_file_info = {
            'unpacked_file_path': 'unpacked_file_path',
            'unpacked_file_name': 'unpacked_file_name'
        }
        :return result: True/Exists or False/Otherwise
        :rtype result: bool
        """
        result = False
        if 'unpacked_file_name' in unpacked_file_info:
            unpacked_file_name = unpacked_file_info['unpacked_file_name']
            if isinstance(unpacked_file_name, str):
                package_version = search("-(\d+\.)(\d+\.)?(\d+)?", unpacked_file_name)                    
                if package_version:
                    package_version_string = package_version.group(0)
                    normalized_file_name = "*"+unpacked_file_name.replace(package_version_string, "")+"*"
                    for file in listdir(self.dest_path):
                        if fnmatch(file, normalized_file_name):
                            result = True
                else:
                    self.logger.error("Problem obtaining version number for %s" % (unpacked_file_name))
            else:
                result = False
                self.logger.error("Wrong unpacked_file_name at checking")
        else:
            self.logger.error("Wrong input format at _is_deb_package_created")
        return result

    def make_packages(self) -> dict:
        """Make deb packages.

        :return: Dict with correct packages.
        :rtype: dict
        """
        result = {}
        self.logger.info("Making packages.")
        self.logger.debug("Creating a temporary directory.")
        with TemporaryDirectory() as tmpdirname:
            settings = {
                'requirements_file': self.requirements_file_path,
                'python_exec': self.python_exec,
                'pip_exec': self.pip_exec,
                'dest_path': self.dest_path,
                'tmp_path': tmpdirname,
                'logger': self.logger,
                'launch_cmd': self.launch_cmd,
                'extract_file': self.extract_file
            }
            package_generator = self.package_generator(settings)
            package_generator.download_requirements()
            self.unpacked_files_info = package_generator.unpack_source_code()
            for unpack_file_info in self.unpacked_files_info:
                is_package_correct = False
                package_generator.make_source_package(unpack_file_info)
                package_generator.make_binary_package(unpack_file_info)
                package_generator.move_binary_package(unpack_file_info)
                if self._is_deb_package_created(unpack_file_info):
                    is_package_correct = True
                result[unpack_file_info['unpacked_file_name']] = is_package_correct
        return result
