

import sys
import logging



class Logger(object):

	def __init__(self, logfile):

		logFormatter = logging.Formatter("NMAP-SEARCH : %(asctime)s :  %(message)s", "%Y-%m-%d %H:%M:%S")
		self.__rootLogger = logging.getLogger()
		self.__rootLogger.setLevel(logging.DEBUG)

		fileHandler = logging.FileHandler(logfile)
		fileHandler.setFormatter(logFormatter)
		self.__rootLogger.addHandler(fileHandler)


	def _logging(self, message, is_exit):

		self.__rootLogger.debug(message)	
		
		if is_exit:
			sys.exit(1)	
		
