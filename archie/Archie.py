from __future__ import print_function
import logging, logging.config, os

from archie.headertiers.businessrules.HeaderReorganization import HeaderReorganization
from archie.headertiers.businessrules.IncludePath import IncludePath
from archie.projectmodel.plugins.OSProjectServices import OSProjectServices
from archie.projectmodel.plugins.YAMLProjectLayout import YAMLProjectLayout

class Archie(object):
    def __init__(self,
                 config_path = '.archie-config',
                 base_include_path = None):
        self.project_layout = self._constructProjectLayout(config_path,
                                                           base_include_path)
        self.project_services = OSProjectServices()
        
    def _constructProjectLayout(self, config_path, base_include_path = None):
        project_layout = YAMLProjectLayout()
        project_layout.loadConfig(config_path)
        if base_include_path != None:
            project_layout.setBaseIncludeFolder(base_include_path)
        return project_layout

    def installHeaderFiles(self):
        reorganization = HeaderReorganization(self.project_layout,
                                              self.project_services)
        reorganization.reorganizeHeaders()

    def getIncludePath(self,
                       source_folder,
                       absolute_paths = False,
                       include_third_party = True,
                       include_tiers = True):
        include_resolver = IncludePath(self.project_layout,
                                       self.project_services)
        path_list = include_resolver.resolveIncludePaths(source_folder,
                                                         include_third_party,
                                                         include_tiers)
        return path_list

    def printIncludePath(self,
    	                 source_folder,
    	                 arg_prefix = '-I',
    	                 absolute_paths = False,
    	                 include_third_party = True,
    	                 third_party_arg_prefix = None):
        if third_party_arg_prefix == None:
        	third_party_arg_prefix = arg_prefix
        if include_third_party:
            third_party_path_list = self.getIncludePath(source_folder,
        	                                            absolute_paths,
        	                                            True,
        	                                            False)
            for path in third_party_path_list:
                print(third_party_arg_prefix + path, end = ' ')
        
        path_list = self.getIncludePath(source_folder,
        	                            absolute_paths,
        	                            False,
        	                            True)
        for path in path_list:
            print(arg_prefix + path, end = ' ')
        print("\n", end = '')

# Configure logging if we find a logging file
if os.path.isfile('.archie-logging.conf'):
    logging.config.fileConfig('.archie-logging.conf')