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
    	
    def test_get_third_party_include_folder_returns_an_empty_list_for_no_folders(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('*/CodeLib', 4, 'code/CodeLib')
    	self.assertEqual([], project.getThirdPartyIncludeFolders(1))
    	
    def test_get_third_party_include_folder_returns_third_party_folders_in_that_tier(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('*/CodeLib', 1, 'code/CodeLib')
    	self.assertEqual(['code/CodeLib'], project.getThirdPartyIncludeFolders(1))
    	
    def test_get_third_party_include_folder_returns_an_empty_list_for_higher_tiers_than_configured(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('*/CodeLib', 1, 'code/CodeLib')
    	self.assertEqual([], project.getThirdPartyIncludeFolders(5))
    	
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

    def test_a_starstar_in_the_pattern_matches_a_dash(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/repository/*.h', 6)
    	self.assertEqual(6, project.tierForModule('Source/Module-1/repository/ISomeInterface.h'))
    	self.assertEqual(1, project.tierForModule('Source/Module-1/repository/ISomeInterfacedoth'))

    def test_a_star_in_the_pattern_matches_a_dash(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/repository/*.h', 6)
    	self.assertEqual(6, project.tierForModule('Source/Module1/repository/I-SomeInterface.h'))
    	self.assertEqual(1, project.tierForModule('Source/Module1/repository/I-SomeInterfacedoth'))
    	
    def test_an_underscore_in_the_pattern_matches_an_underscore(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/repository/I[A-Z]*_h', 6)
    	self.assertEqual(6, project.tierForModule('Source/Module1/repository/ISomeInterface_h'))
    	self.assertEqual(1, project.tierForModule('Source/Module1/repository/ISomeInterfacedoth'))
    	
    def test_a_double_star_can_match_an_empty_directory(self):
        project = ProjectLayout()
        project.addTierForModulesLike('**/afolder', 6)
        self.assertEqual(6, project.tierForModule('afolder'))

    def test_a_double_star_can_match_a_drive_name(self):
        project = ProjectLayout()
        project.addTierForModulesLike('**/afolder', 6)
        self.assertEqual(6, project.tierForModule('C:/afolder'))

    def test_a_double_star_at_the_end_can_match_no_folder(self):
         project = ProjectLayout()
         project.addTierForModulesLike('**/afolder/**', 6)
         self.assertEqual(6, project.tierForModule('afolder'))

    def test_a_double_star_in_the_middle_can_match_no_folder_but_a_separator(self):
         project = ProjectLayout()
         project.addTierForModulesLike('afolder/**/someotherfolder', 6)
         self.assertEqual(6, project.tierForModule('afolder/someotherfolder'))
         self.assertEqual(6, project.tierForModule('afolder/anextrafolder/someotherfolder'))
         self.assertEqual(1, project.tierForModule('thewrongfolder/someotherfolder'))
         self.assertEqual(1, project.tierForModule('afolder/alsothewrongfolder'))

    def test_the_default_tier_is_returned_when_no_configured_tier_is_known(self):
    	project = ProjectLayout()
    	project.setDefaultTier(3)
    	self.assertEqual(3, project.tierForModule('Source/Module1/Plugin'))
    	
    def test_a_module_suffix_can_be_matched_with_double_star_wildcards(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('**/BusinessLogic', 2)
    	self.assertEqual(2, project.tierForModule('Source/Module1/BusinessLogic'))

    def test_a_series_of_matching_tier_rules_are_applied_in_order(self):
    	project = ProjectLayout()
        project.addTierForModulesLike('**/Source/**', 1)
    	project.addTierForModulesLike('**/BusinessLogic/**', 2)
        project.addTierForModulesLike('**/Module1/**', 4)
    	self.assertEqual(4, project.tierForModule('Source/Module1/BusinessLogic'))
    	
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

    def test_a_module_is_by_default_not_third_party(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/BusinessLogic', 2)    	
        self.assertFalse(project.isThirdPartyModule('Source/Module1/Entities'))
        
    def test_a_module_is_able_to_be_configured_not_third_party(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/Entities', 2, None)    	
        self.assertFalse(project.isThirdPartyModule('Source/Module1/Entities'))
        
    def test_a_module_is_able_to_be_configured_third_party(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('*/CodeLib', 2, 'code/CodeLib')    	
        self.assertTrue(project.isThirdPartyModule('code/CodeLib'))
        
    def test_a_module_by_default_has_no_third_party_path(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/BusinessLogic', 2)    	
        self.assertTrue(project.thirdPartyIncludePath('Source/Module1/Entities') == None)
        
    def test_a_module_is_able_to_be_configured_with_no_third_party_path(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/Entities', 2, None)    	
        self.assertTrue(project.thirdPartyIncludePath('Source/Module1/Entities') == None)
        
    def test_a_module_is_able_to_be_configured_with_a_third_party_path(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('*/CodeLib', 2, 'code/CodeLib')    	
        self.assertEqual('code/CodeLib', project.thirdPartyIncludePath('code/CodeLib'))

    def test_the_minimum_reachable_tier_is_normally_one(self):
    	project = ProjectLayout()
    	self.assertEqual(1, project.getMinimumReachableTier(5))
    	
    def test_the_minimum_reachable_tier_is_able_to_be_limited(self):
    	project = ProjectLayout()
    	project.setTierStepLimit(2)
    	self.assertEqual(3, project.getMinimumReachableTier(5))
    	
    def test_the_minimum_reachable_tier_is_never_less_than_one(self):
    	project = ProjectLayout()
    	project.setTierStepLimit(9)
    	self.assertEqual(1, project.getMinimumReachableTier(5))
    	
    def test_setting_a_negative_tier_step_limit_is_truncated_to_no_limit(self):
    	project = ProjectLayout()
    	project.setTierStepLimit(-1)
    	self.assertEqual(1, project.getMinimumReachableTier(5))

    def test_setting_a_zero_tier_step_limit_is_truncated_to_no_limit(self):
    	project = ProjectLayout()
    	project.setTierStepLimit(0)
    	self.assertEqual(1, project.getMinimumReachableTier(5))
    	
    def test_a_module_is_by_default_not_prescient(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/BusinessLogic', 2)    	
        self.assertFalse(project.isPrescientModule('Source/Module1/Entities'))
        
    def test_a_module_is_able_to_be_configured_not_prescient(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('Source/*/Entities', 2, None, False)    	
        self.assertFalse(project.isPrescientModule('Source/Module1/Entities'))
        
    def test_a_module_is_able_to_be_configured_prescient(self):
    	project = ProjectLayout()
    	project.addTierForModulesLike('*/CodeLib', 2, None, True)    	
        self.assertTrue(project.isPrescientModule('code/CodeLib'))