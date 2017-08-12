import unittest

from projectmodel.entities.ProjectLayout import ProjectLayout
from projectmodel.entities.ProjectServices import ProjectServices
from headertiers.businessrules.IncludePath import IncludePath

class StubProjectServices(ProjectServices):
    def __init__(self):
        self.linked_files = dict()
        self.files_lists = dict()
        self.folders_lists = dict()
        
    def createLinkedFile(self, source_file, dest_folder):
        self.linked_files[source_file] = dest_folder
    
    def listFiles(self, folder):
        return self.files_lists[folder]
    
    def listFolders(self, folder):
        return self.folders_lists[folder]

class TestHeaderReorganization(unittest.TestCase):
    def test_reorganize_headers_for_single_module(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = ['Source/Module1/File1.cpp', 'Source/Module1/File1.h', 'Source/Module1/File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['build/include/T1'], path_resolver.resolveIncludePaths('Source/Module1'))
        
    def test_reorganize_headers_for_a_higher_tier_module(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Module2', 3)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module2'] = ['Source/Module2/File1.cpp', 'Source/Module2/File1.h', 'Source/Module2/File2.h']
        services.folders_lists['Source'] = ['Source/Module2']
        services.folders_lists['Source/Module2'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['build/include/T1', 'build/include/T2', 'build/include/T3'], path_resolver.resolveIncludePaths('Source/Module2'))
        
    def test_resolve_include_path_for_module_with_private_headers(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Module2', 3)
        layout.addTierForModulesLike('**/private', -1)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = ['Source/Module1/File1.cpp', 'Source/Module1/File1.h', 'Source/Module1/File2.h']
        services.files_lists['Source/Module1/private'] = ['Source/Module1/private/File1.cpp', 'Source/Module1/private/File1.h', 'Source/Module1/private/File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/private']
        services.folders_lists['Source/Module1/private'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['Source/Module1/private', 'build/include/T1'], path_resolver.resolveIncludePaths('Source/Module1'))        
