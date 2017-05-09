

import os
import re
import shlex
import shutil
import subprocess

from lib.logger import Logger
from lib.searchsploit import SearchSploit
from lib.nmapsearch_exceptions import NmapSearchException


class Nmap(object):


	def __init__(self, logger):

		self.__result = { }

		try:
			self.__searchsploit = SearchSploit(logger)		
		except Exception, err:
			raise NmapSearchException(str(err))


		self.__logger = logger

		self.__nmap = "/usr/bin/nmap"
		if not os.path.exists(self.__nmap):
			raise NmapSearchException("Nmap Path: {0} Doesn't exists !!!".format(self.__nmap))

		port_scan_options = "-n -sV --open -p "
		self.__scan_options = { True:port_scan_options,  False:"-Pn {0}".format(port_scan_options) }

		self.__open_port_regex = re.compile("[0-9]+/open/tcp//")



	def _port_scan(self, ping, ports, network):

		self.__logger._logging("START", False)

		cmd = "{0} {1} {2} {3} -oG -".format(self.__nmap, self.__scan_options[ping], ports, network)
		self.__logger._logging("Running CMD: {0}".format(cmd), False)

		proc = subprocess.Popen(shlex.split(cmd), shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE, )
		
		for line in iter(proc.stdout.readline, ''):
			if re.search(self.__open_port_regex, line):
				ip = line.split()[1]

				for port_service in [ port_service.split("/") for port_service in "".join(data for data in line.split(":")[2:]).split(",") ]:
					service = port_service[6]
					port = port_service[0].strip()

					ip_service = "{0}:{1}".format(ip, service)

					try:
						self.__result[port] = "{0},{1}".format(self.__result[port], ip_service)
					except:
						self.__result[port] = ip_service


		for port, ip_service in self.__result.iteritems():
			for data in ip_service.split(","):
				service = data.split(":")[1]

				if service:
					ip = data.split(":")[0]
					result = self.__searchsploit._run(service)			

					print "{0} - {1}\n{2}\n\n{3}".format(ip, port, len("{0} - {1}".format(ip, port))*"-", result)

		self.__logger._logging("STOP", False)
		
