# -*- coding: utf-8 -*-

import sys
import os.path
import configparser

class Settings(object):
    def __init__(self, settings: dict) -> None:
        """Class constructor.

        settings = dict(
            config_file=CONFIG_FILE,
            dev_config_file=DEV_CONFIG_FILE,
            logger=logger
        )
        :param config: Needed params
        :type config_file: dict
        """
        self.config_file = settings['config_file']
        self.dev_config_file = settings['dev_config_file']
        self.logger = settings['logger']
        self.config = configparser.ConfigParser()
        if os.path.isfile(self.config_file):
            self.config.read([self.config_file])
        elif os.path.isfile(self.dev_config_file):
            self.logger.info('Loading dev config file ./rhea-credentials-manager.conf')
            self.config.read([self.dev_config_file])
        else:
            self.logger.critical('Configuration file not found (rhea-credentials-manager.conf).')
            sys.exit()
        self.logger.debug("Instantiated class %s" % (self.__class__.__name__))


    def get_project_settings(self) -> dict:
        """Get settings like a dict.

        :return: Settings params
        :rtype: dict
        """
        # Get settings options...
        pip_exec = self.config['general']['pip_executable']
        application_settings = {
            'pip_exec': pip_exec
        }
        profiler_settings = {
            "stats_path": os.path.abspath(self.config['profiler']['stats_path']),
            "sort_by": self.config['profiler']['sort_by']
        }
        settings = {
            'application_settings': application_settings,
            'profiler_settings': profiler_settings
        }
        return settings

    def is_profiler_enabled(self) -> bool:
        """Returns profiler status.

        :return: True/Enabled or False/Disabled
        :rtype: bool
        """
        return self.config['profiler'].getboolean('enabled')