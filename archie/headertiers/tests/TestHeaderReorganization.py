import unittest

from projectmodel.entities.ProjectLayout import ProjectLayout
from projectmodel.entities.ProjectServices import ProjectServices
from headertiers.businessrules.HeaderReorganization import HeaderReorganization

class StubProjectServices(ProjectServices):
    def __init__(self):
        self.linked_files = dict()
        self.files_lists = dict()
        self.folders_lists = dict()
        self.file_dates = dict()
        self.removed_files = set()
        
    def createLinkedFile(self, source_file, dest_folder):
        self.linked_files[source_file] = dest_folder
        
    def removeFile(self, file_path):
        self.removed_files.add(file_path)
        
    def folderExists(self, folder_path):
        return folder_path in self.folders_lists
    
    def createFolder(self, folder_path):
        self.folders_lists[folder_path] = []
        self.files_lists[folder_path] = []
        
    def statFile(self, file_path):
        return self.file_dates[file_path]
        
    def fileExists(self, file_path):
    	return file_path in self.file_dates
    
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
        services.files_lists['Source/Module1'] = ['File1.cpp', 'File1.h', 'File2.h']
        services.files_lists['build/include/T1'] = []
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(2, len(services.linked_files))
        self.assertEquals('build/include/T1', services.linked_files['Source/Module1/File1.h'])
        self.assertEquals('build/include/T1', services.linked_files['Source/Module1/File2.h'])
        
    def test_reorganize_headers_when_a_target_folder_is_missing(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = ['File1.cpp', 'File1.h', 'File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertTrue('build/include/T1' in services.files_lists)
        self.assertEquals(2, len(services.linked_files))
        self.assertEquals('build/include/T1', services.linked_files['Source/Module1/File1.h'])
        self.assertEquals('build/include/T1', services.linked_files['Source/Module1/File2.h'])
        
    def test_reorganize_headers_for_a_different_tier_module(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Plugins', 4)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/Plugins'] = ['File1.cpp', 'File1.h', 'File2.h']
        services.files_lists['build/include/T4'] = []        
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/Plugins']
        services.folders_lists['Source/Module1/Plugins'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(2, len(services.linked_files))
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File1.h'])
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File2.h'])
        
    def test_private_headers_are_not_reorganized(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/private', -1)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/private'] = ['File1.cpp', 'File1.h', 'File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/private']
        services.folders_lists['Source/Module1/private'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(0, len(services.linked_files))
        
    def test_headers_which_are_no_longer_in_the_sources_are_removed_from_the_destinations(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Plugins', 4)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/Plugins'] = ['File1.cpp', 'File1.h']
        services.files_lists['build/include/T4'] = ['File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/Plugins']
        services.folders_lists['Source/Module1/Plugins'] = []
        services.folders_lists['build/include/T4'] = []

        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(1, len(services.linked_files))
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File1.h'])
        self.assertEquals(1, len(services.removed_files))
        self.assertTrue('build/include/T4/File2.h' in services.removed_files)
        
    def test_headers_which_are_no_longer_in_the_sources_are_removed_from_the_destinations_even_if_their_tier_folder_is_unused(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Plugins', 4)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/Plugins'] = ['File1.cpp', 'File1.h']
        services.files_lists['build/include/T4'] = ['File2.h']
        services.files_lists['build/include/T3'] = ['File2.h']
        services.files_lists['build/include/T2'] = ['File2.h']
        services.files_lists['build/include/T1'] = ['File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/Plugins']
        services.folders_lists['Source/Module1/Plugins'] = []
        services.folders_lists['build/include/T4'] = []
        services.folders_lists['build/include/T3'] = []
        services.folders_lists['build/include/T2'] = []
        services.folders_lists['build/include/T1'] = []

        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(1, len(services.linked_files))
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File1.h'])
        self.assertEquals(4, len(services.removed_files))
        self.assertTrue('build/include/T4/File2.h' in services.removed_files)
        self.assertTrue('build/include/T1/File2.h' in services.removed_files)
        self.assertTrue('build/include/T2/File2.h' in services.removed_files)
        self.assertTrue('build/include/T3/File2.h' in services.removed_files)
        
    def test_headers_which_are_already_up_to_date_at_the_target_are_not_shifted(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Plugins', 4)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/Plugins'] = ['File1.cpp', 'File1.h', 'File2.h']
        services.files_lists['build/include/T4'] = ['File1.h', 'File2.h']
        services.file_dates['Source/Module1/Plugins/File1.h'] = 'uptodate'
        services.file_dates['Source/Module1/Plugins/File2.h'] = 'uptodate'
        services.file_dates['build/include/T4/File1.h'] = 'uptodate'
        services.file_dates['build/include/T4/File2.h'] = 'uptodate'
        
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/Plugins']
        services.folders_lists['Source/Module1/Plugins'] = []
        services.folders_lists['build/include/T4'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(0, len(services.linked_files))
        
    def test_headers_which_are_out_of_date_at_the_target_are_shifted(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Plugins', 4)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/Plugins'] = ['File1.cpp', 'File1.h', 'File2.h']
        services.files_lists['build/include/T4'] = ['File1.h', 'File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/Plugins']
        services.folders_lists['Source/Module1/Plugins'] = []
        services.file_dates['Source/Module1/Plugins/File1.h'] = 'uptodate'
        services.file_dates['Source/Module1/Plugins/File2.h'] = 'uptodate'
        services.file_dates['build/include/T4/File1.h'] = 'notuptodate'
        services.file_dates['build/include/T4/File2.h'] = 'notuptodate'
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(2, len(services.linked_files))
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File1.h'])
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File2.h'])
        self.assertEquals(2, len(services.removed_files))
        self.assertTrue('build/include/T4/File1.h' in services.removed_files)
        self.assertTrue('build/include/T4/File2.h' in services.removed_files)
        
    def test_reorganize_headers_inside_a_module(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Plugins', 4)
        layout.addTierForModulesLike('**/Plugins/File9.h', 2)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/Plugins'] = ['File1.cpp', 'File1.h', 'File2.h', 'File9.h']
        services.files_lists['build/include/T4'] = []        
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/Plugins']
        services.folders_lists['Source/Module1/Plugins'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(3, len(services.linked_files))
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File1.h'])
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File2.h'])
        self.assertEquals('build/include/T2', services.linked_files['Source/Module1/Plugins/File9.h'])
        
    def test_headers_which_are_no_longer_in_the_sources_are_removed_from_the_destinations_even_if_their_tier_folder_is_unused(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/Plugins', 4)
        layout.addTierForModulesLike('**/Plugins/File9.h', 8)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/Plugins'] = ['File1.cpp', 'File1.h', 'File9.h']
        services.files_lists['build/include/T8'] = ['File2.h', 'File9.h']
        services.files_lists['build/include/T7'] = ['File2.h', 'File9.h']
        services.files_lists['build/include/T6'] = ['File2.h', 'File9.h']
        services.files_lists['build/include/T5'] = ['File2.h', 'File9.h']
        services.files_lists['build/include/T4'] = ['File2.h', 'File9.h']
        services.files_lists['build/include/T3'] = ['File2.h']
        services.files_lists['build/include/T2'] = ['File2.h']
        services.files_lists['build/include/T1'] = ['File2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/Plugins']
        services.folders_lists['Source/Module1/Plugins'] = []
        services.folders_lists['build/include/T8'] = []
        services.folders_lists['build/include/T7'] = []
        services.folders_lists['build/include/T6'] = []
        services.folders_lists['build/include/T5'] = []
        services.folders_lists['build/include/T4'] = []
        services.folders_lists['build/include/T3'] = []
        services.folders_lists['build/include/T2'] = []
        services.folders_lists['build/include/T1'] = []

        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(2, len(services.linked_files))
        self.assertEquals('build/include/T4', services.linked_files['Source/Module1/Plugins/File1.h'])
        self.assertEquals('build/include/T8', services.linked_files['Source/Module1/Plugins/File9.h'])
        self.assertEquals(12, len(services.removed_files))
        self.assertTrue('build/include/T8/File2.h' in services.removed_files)
        self.assertTrue('build/include/T7/File2.h' in services.removed_files)
        self.assertTrue('build/include/T6/File2.h' in services.removed_files)
        self.assertTrue('build/include/T5/File2.h' in services.removed_files)
        self.assertTrue('build/include/T4/File2.h' in services.removed_files)
        self.assertTrue('build/include/T1/File2.h' in services.removed_files)
        self.assertTrue('build/include/T2/File2.h' in services.removed_files)
        self.assertTrue('build/include/T3/File2.h' in services.removed_files)
        self.assertTrue('build/include/T7/File9.h' in services.removed_files)
        self.assertTrue('build/include/T6/File9.h' in services.removed_files)
        self.assertTrue('build/include/T5/File9.h' in services.removed_files)
        self.assertTrue('build/include/T4/File9.h' in services.removed_files)
        
    def test_private_headers_in_a_public_module_are_not_reorganized(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/public', 6)
        layout.addTierForModulesLike('**/public/*_p.h', 0)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/public'] = ['File1_p.cpp', 'File1_p.h', 'File2_p.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/public']
        services.folders_lists['Source/Module1/public'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(0, len(services.linked_files))

    def test_public_headers_in_a_private_module_are_reorganized(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        layout.addTierForModulesLike('**/private', 0)
        layout.addTierForModulesLike('**/private/Public*.h', 4)
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = []
        services.files_lists['Source/Module1/private'] = ['PublicFile1.cpp', 'PublicFile1.h', 'PublicFile2.h']
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = ['Source/Module1/private']
        services.folders_lists['Source/Module1/private'] = []
        
        reorganizer = HeaderReorganization(layout, services)
        
        reorganizer.reorganizeHeaders()
        self.assertEquals(2, len(services.linked_files))
        self.assertTrue('Source/Module1/private/PublicFile1.h' in services.linked_files)
        self.assertTrue('Source/Module1/private/PublicFile2.h' in services.linked_files)