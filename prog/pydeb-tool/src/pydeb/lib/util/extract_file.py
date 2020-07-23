#!/usr/bin/python3.5
"""
.. module:: pydeb.lib.util.extract_file
  :platform: Unix/Linux
  :synopsis: Extracting tools used by code
.. moduleauthor:: Isaac Pena, Ismael Narvaez
  :Nickname: ipena, inarvaez
  :mail: ipena@wtelecom.es, inarvaez@wtelecom.es
  :Web : github.com
"""
import tarfile
from zipfile import ZipFile
from os.path import join, abspath
from typing import Union

def extract_file(settings: dict) -> Union[str, bool]:
    """Extract .tar.gz, .tar or .zip.

        settings = {
            'filename': 'filename',
            'dest_path': 'dest_path',
            'logger': 'logger'
        }
        :param settings: Class dependencies
        :type settings: dict
    """
    filename = settings['filename']
    dest_path = settings['dest_path']
    logger = settings['logger']
    result = False
    try:
        if (filename.endswith(".tar.gz")):
            safe_file = is_tar_safe(filename, dest_path, "r:gz")
            if safe_file:
                extract_tar(filename, dest_path, "r:gz")
                logger.info("Extracted %s into %s" % (filename, dest_path))
                result = filename.replace(".tar.gz", "")
            else:
                result = False
        elif (filename.endswith(".tar")):
            safe_file = is_tar_safe(filename, dest_path, "r:")
            if safe_file:
                extract_tar(filename, dest_path, "r:")
                logger.info("Extracted %s into %s" % (filename, dest_path))
                result = filename.replace(".tar", "")
            else:
                result = False
        elif (filename.endswith(".tar.bz2")):
            safe_file = is_tar_safe(filename, dest_path, "r:bz2")
            if safe_file:
                extract_tar(filename, dest_path, "r:bz2")
                logger.info("Extracted %s into %s" % (filename, dest_path))
                result = filename.replace(".tar.bz2", "")
            else:
                result = False
        elif (filename.endswith(".zip")):
            extract_zip(filename, dest_path)
            result = filename.replace(".zip", "")
            logger.info("Extracted %s into %s" % (filename, dest_path))
        else:
            pass
    except Exception as e:
        logger.exception(e)
    return result


def is_tar_safe(tar_file_name, dest_path, mode):
    """
    Check is safe untar a file.
    
    :param tar_file_name: File checked
    :type tar_file_name: str
    :param dest_path: Destination path
    :type dest_path: str
    :param mode: Read mode
    :type mode: str
    """
    safe_file = True
    with tarfile.open(tar_file_name, mode) as tarf:
        for names in tarf.getnames():
            if not abspath(join(dest_path, names)).startswith(dest_path):
                safe_file = False
    return safe_file


def extract_tar(tar_file_name, dest_path, mode):
    """Extract a tar file in a specific location.

    :param tar_file_name: File checked
    :type tar_file_name: str
    :param dest_path: Destination path
    :type dest_path: str
    :param mode: Read mode
    :type mode: str
    """
    with tarfile.open(tar_file_name, mode) as tarf:
        tarf.extractall(path=dest_path)

def extract_zip(zip_file_name, dest_path):
    """Extract a zip file in a specific location.

    :param zip_file_name: File checked
    :type zip_file_name: str
    :param dest_path: Destination path
    :type dest_path: str
    """
    with ZipFile(zip_file_name) as zipf:
        for element in zipf.infolist():
            zipf.extract(element, path=dest_path)
