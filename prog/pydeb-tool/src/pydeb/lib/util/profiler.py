#!/usr/bin/python3.5
"""
.. module:: pydeb.lib.utils.profiler
  :platform: Unix/Linux
  :synopsis: Profiler used with our project
.. moduleauthor:: Ismael Narvaez
  :Nickname: inarvaez
  :mail: inarvaez@wtelecom.es
  :Web : github.com
"""
import os
import cProfile
import pstats
import io
from datetime import datetime

class Profiler(object):
    """Provide a profiler to get performance info."""

    def __init__(self, settings: dict) -> None:
        """Class constructor.

        settings = {
            "stats_path": "/path",
            "sort_by": "filename"
        }
        :param settings: Profiler settings
        :type settings: dict 
        """
        self.stats_path = settings['stats_path']
        if not os.path.exists(self.stats_path):
            os.makedirs(self.stats_path)
        self.filename = "profiler-" + str(datetime.utcnow()).replace(" ", "_")
        self.sort_by = settings['sort_by']
        self.profiler = cProfile.Profile()
    
    def start(self) -> None:
        """Starts profiler."""
        self.profiler.enable()
    
    def stop(self) -> None:
        """Stops profiler."""
        self.profiler.disable()
        self._save_data()

    def _save_data(self) -> None:
        """Save data using our location."""
        stream = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=stream)\
            .sort_stats(self.sort_by)
        ps.print_stats()
        with open(self.stats_path+"/"+self.filename+".profiler", 'w+') as f:
            f.write(stream.getvalue())