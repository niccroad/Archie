import unittest

from projectmodel.entities.ProjectLayout import ProjectLayout

class TestProjectLayout(unittest.TestCase):
    def test_a_source_folder_can_be_added(self):
        project = ProjectLayout()
        project.addSourceFolder('Source/Feature1')
        self.assertListEqual(['Source/Feature1'], project.getSourceFolders())
        
    def test_multiple_source_folders_can_be_added(self):
        project = ProjectLayout()
        project.addSourceFolder('Source/Feature1')
        project.addSourceFolder('Source/Feature2')
        project.addSourceFolder('Source/Feature3')
        self.assertListEqual(['Source/Feature1', 'Source/Feature2', 'Source/Feature3'], project.getSourceFolders())
        
    def test_get_include_path_for_tier(self):
    	project = ProjectLayout()
    	project.setBaseIncludeFolder('Build/include')
    	self.assertEqual('Build/include/T1', project.getIncludeFolder(1))
    
    def test_get_include_path_for_renamed_tier(self):
    	project = ProjectLayout()
    	project.setBaseIncludeFolder('Build/include')
    	project.setTierFolder(2, 'BusinessRules')
    	self.assertEqual('Build/include/BusinessRules', project.getIncludeFolder(2))
    	
    def test_get_include_folder_correct_when_multiple_tiers_requested(self):
    	project = ProjectLayout()
    	project.setBaseIncludeFolder('Build/include')
    	self.assertEqual('Build/include/T1', project.getIncludeFolder(1))
    	self.assertEqual('Build/include/T4', project.getIncludeFolder(4))    	
    	
    def test_a_dot_h_file_is_an_include_file(self):
    	project = ProjectLayout()
    	self.assertTrue(project.isIncludeFile('Source/Module1/File.h'))
    	
    def test_a_dot_hpp_file_is_an_include_file(self):
    	project = ProjectLayout()
    	self.assertTrue(project.isIncludeFile('Source/Module1/File.hpp'))
    	
    def test_another_extension_can_be_added_to_includes(self):
    	project = ProjectLayout()
    	project.addHeaderPattern('*.i')
    	self.assertTrue(project.isIncludeFile('Source/Module1/File.i'))
    	
    def test_dots_in_extensions_are_escaped(self):
    	project = ProjectLayout()
    	project.addHeaderPattern('*.i')
    	self.assertFalse(project.isIncludeFile('Source/Module1/Fileai'))    	
    	
    def test_a_dot_cpp_file_is_not_an_include_file(self):
    	project = ProjectLayout()
    	self.assertFalse(project.isIncludeFile('Source/Module1/File.cpp'))
    	
    def test_a_default_tier_is_returned_for_a_module_when_none_is_configured(self):
    	project = ProjectLayout()
    	self.assertEqual(1, project.tierForModule('Source/Module1/Entity'))
    	
    def test_a_non_default_tier_can_be_configured_and_returned_for_a_module(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/BusinessLogic', 2)
    	self.assertEqual(2, project.tierForModule('Source/Module1/BusinessLogic'))
    	
    def test_a_negative_value_can_be_used_for_a_private_tier(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/private', -1)
    	self.assertEqual(0, project.tierForModule('Source/Module1/private'))
    	
    def test_a_file_pattern_can_be_mapped_to_its_own_tier(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/repository/I[A-Z]*.h', 7)
    	self.assertEqual(7, project.tierForModule('Source/Module1/repository/ISomeInterface.h'))
    	
    def test_a_dot_in_the_pattern_only_matches_a_dot(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/repository/I[A-Z]*.h', 6)
    	self.assertEqual(6, project.tierForModule('Source/Module1/repository/ISomeInterface.h'))
    	self.assertEqual(1, project.tierForModule('Source/Module1/repository/ISomeInterfacedoth'))
    	
    def test_an_underscore_in_the_pattern_matches_any_character(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/repository/I[A-Z]*_h', 6)
    	self.assertEqual(6, project.tierForModule('Source/Module1/repository/ISomeInterface.h'))
    	self.assertEqual(6, project.tierForModule('Source/Module1/repository/ISomeInterfacedoth'))
    	
    def test_a_double_star_can_match_an_empty_directory(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/afolder', 6)
    	self.assertEqual(6, project.tierForModule('afolder'))
    	
    def test_the_default_tier_is_returned_when_no_configured_tier_is_known(self):
    	project = ProjectLayout()
    	project.setDefaultTier(3)
    	self.assertEqual(3, project.tierForModule('Source/Module1/Plugin'))
    	
    def test_a_module_suffix_can_be_matched_with_double_star_wildcards(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/BusinessLogic', 2)
    	self.assertEqual(2, project.tierForModule('Source/Module1/BusinessLogic'))
    	
    def test_a_module_suffix_can_be_unmatched_matched_with_double_star_wildcards(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/BusinessLogic', 2)    	
        self.assertEqual(1, project.tierForModule('Source/Module1/Entities'))

    def test_a_module_suffix_can_be_matched_with_single_star_wildcards(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/BusinessLogic', 2)
    	self.assertEqual(2, project.tierForModule('Source/Module1/BusinessLogic'))
    	
    def test_a_module_suffix_can_be_unmatched_matched_with_single_star_wildcards(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/BusinessLogic', 2)
        self.assertEqual(1, project.tierForModule('Source/Module1/Entities'))

    def test_a_module_suffix_can_be_unmatched_by_intermediates_matched_with_single_star_wildcards(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/BusinessLogic', 2)    	
        self.assertEqual(1, project.tierForModule('Source/Module1/Entities'))
