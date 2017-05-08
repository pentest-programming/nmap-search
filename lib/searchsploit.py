

import os
import re
import shlex
import subprocess

from lib.nmapsearch_exceptions import NmapSearchException


class SearchSploit(object):

	def __init__(self, logger):

		self.__logger = logger

		self.__searchsploit_path = "/usr/bin/searchsploit"		
		if not os.path.exists(self.__searchsploit_path):
			raise NmapSearchException("{0} File Does't Exists".format(self.__searchsploit_path))
		


	def _run(self, service):

		result = ""

		service = re.sub("\s[a-zA-Z]+d\s", " ", service)
		cmd = "{0} \"{1}\"".format(self.__searchsploit_path, service)

		self.__logger._logging("Running SearchSploit CMD: {0}".format(cmd), False)

		proc = subprocess.Popen(shlex.split(cmd), shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE, )

                for line in iter(proc.stdout.readline, ''):
			if ( (not line.startswith("-")) and ( not line.startswith(" ")) and (not line.startswith("\n"))):
				if result:
					result += line
				else:
					result = line

		return result
		



