import os, unittest

from projectmodel.plugins.OSProjectServices import OSProjectServices

class TestOSProjectServices(unittest.TestCase):
    def test_call_move_header(self):
        if not os.path.isdir('build/test'):
            os.makedirs('build/test')
        if os.path.isfile('build/test/File1.h'):
        	os.unlink('build/test/File1.h')
        
        services = OSProjectServices()
        services.createLinkedFile('archie/projectmodel/testdata/source/File1.h', 'build/test')
        
        self.assertTrue(os.path.isfile('build/test/File1.h'))
        
    def test_folder_exists_is_true_for_an_existing_folder_ending_in_slash(self):
        services = OSProjectServices()
        self.assertTrue(services.folderExists('archie/projectmodel/testdata/source/'))
        
    def test_folder_exists_is_true_for_an_existing_folder_ending_before_slash(self):
        services = OSProjectServices()
        self.assertTrue(services.folderExists('archie/projectmodel/testdata/source'))
        
    def test_folder_exists_is_false_for_a_missing_folder(self):
        services = OSProjectServices()
        self.assertFalse(services.folderExists('this/folder/does/not/exist'))
        
    def test_create_folder_creates_a_folder(self):
        services = OSProjectServices()
        if os.path.isdir('build/foldertest'):
            os.rmdir('build/foldertest')
        services.createFolder('build/foldertest')
        
    def test_call_move_header_over_existing_file(self):
        if not os.path.isdir('build/test'):
            os.makedirs('build/test')
        if os.path.isfile('build/test/File1.h'):
        	os.unlink('build/test/File1.h')
        
        services = OSProjectServices()
        services.createLinkedFile('archie/projectmodel/testdata/source/File1.h', 'build/test')
        services.createLinkedFile('archie/projectmodel/testdata/source/File1.h', 'build/test')
        
        self.assertTrue(os.path.isfile('build/test/File1.h'))
        
    def test_a_file_can_be_found_to_exist(self):
    	services = OSProjectServices()
    	self.assertTrue(services.fileExists('archie/projectmodel/testdata/source/File1.h'))
    	
    def test_a_file_can_be_found_to_not_exist(self):
    	services = OSProjectServices()
    	self.assertFalse(services.fileExists('archie/projectmodel/testdata/source/File13.h'))
        
    def test_can_stat_an_existing_file(self):
    	services = OSProjectServices()
    	stat = services.statFile('archie/projectmodel/testdata/source/File1.h')
    	self.assertTrue(stat != None)
        
    def test_list_files(self):
        services = OSProjectServices()
        files = services.listFiles('archie/projectmodel/testdata/source')
        self.assertEquals(['File1.cpp', 'File1.h'], files)
        
    def test_list_files_ending_in_slash(self):
        services = OSProjectServices()
        files = services.listFiles('archie/projectmodel/testdata/source/')
        self.assertEquals(['File1.cpp', 'File1.h'], files)        
        
    def test_list_folders(self):
        services = OSProjectServices()
        folders = services.listFolders('archie/projectmodel')
        self.assertEquals(['archie/projectmodel/entities',
                           'archie/projectmodel/plugins',
                           'archie/projectmodel/testdata',
                           'archie/projectmodel/tests'],
                          folders)
        
    def test_list_folders_ending_in_slash(self):
        services = OSProjectServices()
        folders = services.listFolders('archie/projectmodel/')
        self.assertEquals(['archie/projectmodel/entities',
                           'archie/projectmodel/plugins',
                           'archie/projectmodel/testdata',
                           'archie/projectmodel/tests'],
                          folders)
        