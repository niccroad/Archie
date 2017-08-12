import unittest

from projectmodel.plugins.YAMLProjectLayout import YAMLProjectLayout

class TestYAMLProjectLayout(unittest.TestCase):
    def test_a_yaml_project_layout_can_be_loaded_from_file(self):
    	config = YAMLProjectLayout()
    	config.loadConfig('archie/projectmodel/testdata/Config1.yml')
    	self.assertEquals(['Source', 'TestSource'], config.getSourceFolders())
    	self.assertEquals('include/T1', config.getIncludeFolder(1))
    	self.assertEquals(1, config.tierForModule('Source/Module1/Entities'))
    	self.assertEquals(2, config.tierForModule('Source/Module1/BusinessRules'))
    	self.assertEquals(3, config.tierForModule('Source/Module1/Interfaces'))
    	self.assertEquals(4, config.tierForModule('Source/Module1/Plugins'))
    	self.assertEquals(5, config.tierForModule('Source/Module1/TestCases'))
    	self.assertEquals(0, config.tierForModule('Source/Module1/private'))
    	
    def test_a_yaml_project_layout_can_be_loaded_from_file_with_a_private_module_by_name(self):
    	config = YAMLProjectLayout()
    	config.loadConfig('archie/projectmodel/testdata/Config2.yml')
    	self.assertEquals(['Source', 'TestSource'], config.getSourceFolders())
    	self.assertEquals('include/T1', config.getIncludeFolder(1))
    	self.assertEquals(1, config.tierForModule('Source/Module1/Entities'))
    	self.assertEquals(2, config.tierForModule('Source/Module1/BusinessRules'))
    	self.assertEquals(3, config.tierForModule('Source/Module1/Interfaces'))
    	self.assertEquals(4, config.tierForModule('Source/Module1/Plugins'))
    	self.assertEquals(5, config.tierForModule('Source/Module1/TestCases'))
    	self.assertEquals(0, config.tierForModule('Source/Module1/private'))    	
    	
    def test_a_yaml_project_layout_can_be_loaded_from_file_when_no_include_folder_is_configured(self):
    	config = YAMLProjectLayout()
    	config.loadConfig('archie/projectmodel/testdata/ConfigDefaultBaseInclude.yml')
    	self.assertEquals(['Source', 'TestSource'], config.getSourceFolders())
    	self.assertEquals('build/include/T1', config.getIncludeFolder(1))
    	
    def test_a_yaml_project_layout_can_be_loaded_from_file_when_no_source_folders_are_configured(self):
    	config = YAMLProjectLayout()
    	config.loadConfig('archie/projectmodel/testdata/ConfigDefaultSourceFolders.yml')
    	self.assertEquals([], config.getSourceFolders())
    	self.assertEquals('include/T1', config.getIncludeFolder(1))
    	
    def test_a_yaml_project_layout_can_be_loaded_from_file_with_a_misspelled_string_tier(self):
    	config = YAMLProjectLayout()
    	config.loadConfig('archie/projectmodel/testdata/ConfigMisspecifiedStringTier.yml')
    	self.assertEquals(['Source', 'TestSource'], config.getSourceFolders())
    	self.assertEquals('include/T1', config.getIncludeFolder(1))
    	self.assertEquals(1, config.tierForModule('Source/Module1/Entities'))
    	self.assertEquals(2, config.tierForModule('Source/Module1/BusinessRules'))
    	self.assertEquals(3, config.tierForModule('Source/Module1/Interfaces'))
    	self.assertEquals(4, config.tierForModule('Source/Module1/Plugins'))
    	self.assertEquals(5, config.tierForModule('Source/Module1/TestCases'))
    	self.assertEquals(5, config.tierForModule('Source/Module1/private'))    	
