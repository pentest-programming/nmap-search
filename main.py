#!/usr/bin/env python


import os
import sys
import signal
import argparse

from lib.nmap import Nmap
from lib.logger import Logger
from lib.config_parser import ConfigParser



class NmapSearch(object):

	def __init__(self):

		parser = argparse.ArgumentParser()

		parser.add_argument('-p', '--ping', dest = 'ping', action = 'store_true', help = 'Ping', default = False)
		parser.add_argument('-n', '--network', dest = 'network', action = 'store', help = 'Network', required = True)
		parser.add_argument('-c', '--config', dest = 'config', action = 'store', help = 'Config File', required = True)		
		parser.add_argument('-l', '--logfile', dest = 'logfile', action = 'store', help = 'Log File', required = True)		

		args = parser.parse_args()

		self.__ping = args.ping
		self.__network = args.network
		self.__logfile = args.logfile
		self.__config_file = args.config

		signal.signal(signal.SIGINT, self.__signal_handler)		

		self.__logger = Logger(self.__logfile)


		if not os.path.exists(self.__config_file):
			self.__logger._logging("File: {0} Doesn't exists !!!".format(self.__config_file), True)
		
		
		self.__port_list = ConfigParser._parser(self.__config_file)

		try:
			self.__nmap = Nmap(self.__logger)
		except Exception, err:
			self.__logger._logging(str(err), True)

		
		try:
			self.__port_list = ConfigParser._parser(self.__config_file)
			self.__nmap = Nmap(self.__logger)
		except Exception, err:
			self.__logger._logging(str(err), True)
	


	def _run(self):

		self.__nmap._port_scan(self.__ping, self.__port_list, self.__network)


	def __signal_handler(self, signal, frame):
        	print('See You - Nmap-Search ...')
        	sys.exit(37)

##
### Main ...
##

if __name__ == "__main__":

	nmap_search = NmapSearch()
	nmap_search._run()

