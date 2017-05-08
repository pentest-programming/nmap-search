

import yaml

from nmapsearch_exceptions import NmapSearchException



class ConfigParser(object):

	__result = None

	@staticmethod
        def _parser(config_file):

		if not ConfigParser.__result:

			try:
				with open(config_file, 'r') as stream:
    					cfg = yaml.load(stream)
			except Exception, err:
				raise NmapSearchException("{0} cannot be opened - {1}".format(config_file, err))			
 

			try:
				port_list = ",".join([ port for port in  set([ ports.strip() for ports in [ value for value in cfg["ports"] ][0].split(",") ]) ])
			except Exception, err:
				raise NmapSearchException("{0} cannot iterate config file - {1}".format(config_file, err))	

			ConfigParser.__result = port_list

		return ConfigParser.__result 



