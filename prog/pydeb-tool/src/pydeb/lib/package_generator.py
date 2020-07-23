#!/usr/bin/python3.5
"""
.. module:: pydeb.lib.package_generator
  :platform: Unix/Linux
  :synopsis: Package generator class
.. moduleauthor:: Ismael Narvaez Berenjeno
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com/wtelecom
"""
from fnmatch import fnmatch
from os import listdir
from os.path import isfile, isdir, join, basename, abspath
from os import environ


class PackageGenerator(object):
    """ Class used to generate debian packages using Pypy packages."""

    def __init__(self, settings: dict) -> None:
        """Class constructor..

        settings = {
            'requirements_file': 'requirements_file',
            'python_exec': 'python_exec_name',
            'pip_exec': 'pip_exec_name',
            'dest_path': 'dest_path',
            'tmp_path': 'tmpdirname',
            'logger': logger,
            'launch_cmd': launch_cmd,
            'extract_file': extract_file
        }
        :param settings: Class dependencies
        :type settings: dict
        """
        self.requirements_file = settings['requirements_file']
        self.python_exec = settings['python_exec']
        self.pip_exec = settings['pip_exec']
        self.dest_path = settings['dest_path']
        self.tmp_path = settings['tmp_path']
        self.launch_cmd = settings['launch_cmd']
        self.extract_file = settings['extract_file']
        self.logger = settings['logger']
        self.logger.debug("Instantiated class %s" % (self.__class__.__name__))

    def download_requirements(self) -> bool:
        """
        Download requirements from pip.

        :return: Return True if successful, False otherwise
        :rtype: bool
        """
        if all(
            isinstance(item, str)
            for item in [self.pip_exec, self.requirements_file, self.tmp_path]):
            self.logger.info("Downloading requirements.")
            cmd = [
                self.pip_exec,
                "download",
                "--no-binary",
                ":all:",
                "-r",
                self.requirements_file,
                "-d",
                self.tmp_path
            ]
            result = self.launch_cmd(cmd, self.logger)
        else:
            result = False
            self.logger.error("Wrong params format used in download_requirements")
        return result

    def unpack_source_code(self) -> bool:
        """
        Unpack downloaded packages.

        :return: List with all info related to unpacked files
        :rtype: list
        """
        unpacked_files = []

        try:
            is_dir_tmp_path = isdir(self.tmp_path)
        except Exception as e:
            self.logger.exception(e)
            is_dir_tmp_path = False

        if isinstance(self.tmp_path, str) and is_dir_tmp_path:
            self.logger.info("Unpacking packages.")
            files_in_path = [
                join(self.tmp_path, f)
                for f in listdir(self.tmp_path)
                    if isfile(join(self.tmp_path, f))
            ]
            for file in files_in_path:
                unpacked_file_info = {
                    'unpacked_file_name': None,
                    'unpacked_file_path': None
                }
                settings = {
                    'filename': file,
                    'dest_path': self.tmp_path,
                    'logger': self.logger
                }
                unpacked_file_path = self.extract_file(settings)
                if isinstance(unpacked_file_path, str):
                    unpacked_file_info['unpacked_file_path'] = unpacked_file_path
                    unpacked_file_info['unpacked_file_name'] = basename(unpacked_file_path)
                    unpacked_files.append(unpacked_file_info)
        else:
            self.logger.error("Error with params format used in unpack_source_code")
        return unpacked_files
    
    def make_source_package(self, unpacked_file_info: dict) -> bool:
        """
        Make source package.

        unpacked_file_info = {
            'unpacked_file_path': 'unpacked_file_path',
            'unpacked_file_name': 'unpacked_file_name'
        }
        :return: True if successful, False otherwise
        :rtype: bool
        """
        result = False
        if isinstance(unpacked_file_info, dict) and \
            ('unpacked_file_path' in unpacked_file_info):
            unpacked_file_path = unpacked_file_info['unpacked_file_path']
            if all(isinstance(item, str) for item in [unpacked_file_path, self.python_exec]):
                self.logger.info("Making source package for %s" % str(unpacked_file_path))
                current_working_directory = abspath(unpacked_file_path)
                clean_pyc_cmd = [
                    "find",
                    unpacked_file_path,
                    "-name",
                    "*.pyc",
                    "-type",
                    "f",
                    "-delete"
                ]
                build_cmd = [
                    self.python_exec,
                    "setup.py",
                    "--command-packages=stdeb.command",
                    "sdist_dsc"
                ]
                result_clean_pyc = self.launch_cmd(
                    clean_pyc_cmd,
                    self.logger
                )
                result = self.launch_cmd(
                    build_cmd,
                    self.logger,
                    cwd=current_working_directory
                )
            else:
                self.logger.error("Wrong params format.")
        else:
            self.logger.error("Wrong input dictionary.")
        return result

    def make_binary_package(self, unpacked_file_info: dict) -> bool:
        """
        Make binary package.

        unpacked_file_info = {
            'unpacked_file_path': 'unpacked_file_path',
            'unpacked_file_name': 'unpacked_file_name'
        }
        :return: Return True if successful, False otherwise
        :rtype: bool
        """
        result = False
        if isinstance(unpacked_file_info, dict) and \
            ('unpacked_file_path' in unpacked_file_info) and \
            ('unpacked_file_name' in unpacked_file_info):
            unpacked_file_path = unpacked_file_info['unpacked_file_path']
            unpacked_file_name = unpacked_file_info['unpacked_file_name']
            if all(isinstance(item, str) for item in [unpacked_file_path, unpacked_file_name]):
                self.logger.info("Making binary package for %s" % str(unpacked_file_path))
                current_working_directory = abspath(unpacked_file_path) +\
                    "/" + "deb_dist" + "/" + unpacked_file_name
                custom_env = environ.copy()
                custom_env['DEB_BUILD_OPTIONS'] = "nocheck"
                cmd = [
                    "dpkg-buildpackage",
                    "-rfakeroot",
                    "-us",
                    "-uc"
                ]
                result = self.launch_cmd(
                    cmd,
                    self.logger,
                    cwd=current_working_directory,
                    env=custom_env
                )
            else:
                self.logger.error("Wrong params format.")
        else:
            self.logger.error("Wrong input dictionary.")
        return result

    def move_binary_package(self, unpacked_file_info: dict) -> bool:
        """
        Move binary packages to correct location.

        unpacked_file_info = {
            'unpacked_file_path': 'unpacked_file_path',
            'unpacked_file_name': 'unpacked_file_name'
        }
        :return: Return True if successful, False otherwise
        :rtype: bool
        """
        result = False
        if isinstance(unpacked_file_info, dict) and \
            ('unpacked_file_path' in unpacked_file_info) and \
            ('unpacked_file_name' in unpacked_file_info):
            unpacked_file_path = unpacked_file_info['unpacked_file_path']
            unpacked_file_name = unpacked_file_info['unpacked_file_name']
            if all(isinstance(item, str) for item in [unpacked_file_path, unpacked_file_name, self.dest_path]):
                self.logger.info(
                    "Moving binary package %s to %s" %
                    (str(unpacked_file_name), str(self.dest_path))
                )
                current_working_directory = abspath(unpacked_file_path) +\
                    "/" + "deb_dist" + "/"
                if isdir(current_working_directory):
                    for file in listdir(current_working_directory):
                        if fnmatch(file, "*.deb"):
                            cmd = [
                                "mv",
                                file,
                                self.dest_path
                            ]
                            result = self.launch_cmd(
                                cmd,
                                self.logger,
                                cwd=current_working_directory
                            )
            else:
                self.logger.error("Wrong params format.")
        else:
            self.logger.error("Wrong input dictionary.")
        return result