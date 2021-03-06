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

    def test_resolve_include_path_for_module_with_third_party_headers(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Module1', 3)
        layout.addTierForModulesLike('CoreLib', 3, 'CoreLib')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = ['Source/Module1/File1.cpp', 'Source/Module1/File1.h', 'Source/Module1/File2.h']
        services.files_lists['Source/Module1/private'] = ['Source/Module1/private/File1.cpp', 'Source/Module1/private/File1.h', 'Source/Module1/private/File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/private']
        services.folders_lists['Source/Module1/private'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['CoreLib', 'build/include/T1', 'build/include/T2', 'build/include/T3'], path_resolver.resolveIncludePaths('Source/Module1'))
        
    def test_resolve_include_path_for_module_with_lower_tier_third_party_headers(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Module1', 3)
        layout.addTierForModulesLike('CoreLib', 1, 'CoreLib')
        layout.addTierForModulesLike('RenderLib', 2, 'RenderLib')
        layout.addTierForModulesLike('DBLib', 3, 'DBLib')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = ['Source/Module1/File1.cpp', 'Source/Module1/File1.h', 'Source/Module1/File2.h']
        services.files_lists['Source/Module1/private'] = ['Source/Module1/private/File1.cpp', 'Source/Module1/private/File1.h', 'Source/Module1/private/File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/private']
        services.folders_lists['Source/Module1/private'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['CoreLib', 'RenderLib', 'DBLib', 'build/include/T1', 'build/include/T2', 'build/include/T3'], path_resolver.resolveIncludePaths('Source/Module1'))
        
    def test_resolve_include_path_for_a_higher_tier_module_with_reach_limit(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.setTierStepLimit(1)
        layout.addTierForModulesLike('**/Module2', 3)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module2'] = ['Source/Module2/File1.cpp', 'Source/Module2/File1.h', 'Source/Module2/File2.h']
        services.folders_lists['Source'] = ['Source/Module2']
        services.folders_lists['Source/Module2'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['build/include/T2', 'build/include/T3'], path_resolver.resolveIncludePaths('Source/Module2'))

    def test_resolve_include_path_for_module_with_lower_tier_third_party_headers_and_a_reach_limit(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.setTierStepLimit(1)
        layout.addTierForModulesLike('**/Module1', 3)
        layout.addTierForModulesLike('CoreLib', 1, 'CoreLib')
        layout.addTierForModulesLike('RenderLib', 2, 'RenderLib')
        layout.addTierForModulesLike('DBLib', 3, 'DBLib')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = ['Source/Module1/File1.cpp', 'Source/Module1/File1.h', 'Source/Module1/File2.h']
        services.files_lists['Source/Module1/private'] = ['Source/Module1/private/File1.cpp', 'Source/Module1/private/File1.h', 'Source/Module1/private/File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/private']
        services.folders_lists['Source/Module1/private'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['RenderLib', 'DBLib', 'build/include/T2', 'build/include/T3'], path_resolver.resolveIncludePaths('Source/Module1'))
        
    def test_reorganize_headers_for_a_prescient_module(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Module2', 3, None, True)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module2'] = ['Source/Module2/File1.cpp', 'Source/Module2/File1.h', 'Source/Module2/File2.h']
        services.folders_lists['Source'] = ['Source/Module2']
        services.folders_lists['Source/Module2'] = []
        
        path_resolver = IncludePath(layout, services)
        self.assertEqual(['build/include/T0',
                          'build/include/T1',
                          'build/include/T2',
                          'build/include/T3'],
                         path_resolver.resolveIncludePaths('Source/Module2'))
        