from __future__ import print_function
import argparse, logging, logging.config, os

from archie.headertiers.businessrules.HeaderReorganization import HeaderReorganization
from archie.headertiers.businessrules.IncludePath import IncludePath
from archie.projectmodel.plugins.OSProjectServices import OSProjectServices
from archie.projectmodel.plugins.YAMLProjectLayout import YAMLProjectLayout

class Archie(object):
    def __init__(self, config_path = '.archie-config', base_include_path = None):
        self.project_layout = self._constructProjectLayout(config_path, base_include_path)
        self.project_services = OSProjectServices()
        
    def _constructProjectLayout(self, config_path, base_include_path = None):
        project_layout = YAMLProjectLayout()
        project_layout.loadConfig(config_path)
        if base_include_path != None:
            project_layout.setBaseIncludeFolder(base_include_path)
        return project_layout

    def installHeaderFiles(self):
        reorganization = HeaderReorganization(self.project_layout, self.project_services)
        reorganization.reorganizeHeaders()

    def getIncludePath(self, source_folder, absolute_paths = False):
        include_resolver = IncludePath(self.project_layout, self.project_services)
        path_list = include_resolver.resolveIncludePaths(source_folder)
        return path_list

    def printIncludePath(self, source_folder, arg_prefix, absolute_paths = False):
        path_list = self.getIncludePath(source_folder, absolute_paths)
        for path in path_list:
            print(arg_prefix + path, end = ' ')
        print("\n", end = '')

def main():
    parser = argparse.ArgumentParser(description='Build architecture enforcer.')
    parser.add_argument('--install_headers', dest='install_headers', action='store_true', help='install header files from source paths to build paths')
    parser.add_argument('--show_include_path', dest='source_folder', nargs='?', action='store', help='print the include paths which should be used when compiling source folder')
    parser.add_argument('--config', dest='arch_config', nargs='?', action='store', default='.archie_config', type=str, help='architecture configuration file, defaults to .archie_config')
    parser.add_argument('--arg_prefix', dest='arg_prefix', nargs='?', action='store', default='-I', help='argument prefix to use for includes, defaults to -I')
    parser.add_argument('--absolute', dest='abs_paths', action='store_true', help='convert all include paths to absolute paths')
    parser.add_argument('--include_folder', dest='include_folder', nargs='?', action='store', type=str, help='build folder where headers are installed to')    
    args = parser.parse_args()

    archie = Archie(args.arch_config, args.include_folder)

    if args.install_headers:
        archie.installHeaderFiles()
    if args.source_folder != None:
        archie.printIncludePath(args.source_folder, args.arg_prefix)

# Configure logging if we find a logging file
if os.path.isfile('.archie-logging.conf'):
    logging.config.fileConfig('.archie-logging.conf')

if __name__ == "__main__":
    main()
