# -*- coding: utf-8 -*-
import sys
import os.path
import logging
import logging.config

CONFIG_FILE = '/etc/pydeb/logging.conf'
DEV_CONFIG_FILE = './logging.conf'

config_file = None
if os.path.isfile(CONFIG_FILE):
    config_file = CONFIG_FILE
elif os.path.isfile(DEV_CONFIG_FILE):
    print(' - Loading dev logging config file ./logging.conf - ')
    config_file = DEV_CONFIG_FILE

if config_file is not None:
    logging.config.fileConfig(config_file)
    logger = logging.getLogger('root')
else:
    # Default logging config
    logging.basicConfig(level=logging.WARN)
    logging.error('Logging configuration file not found (logging.conf).')
    logger = logging
