import yaml

from archie.projectmodel.entities.ProjectLayout import ProjectLayout

class YAMLProjectLayout(ProjectLayout):
    def loadConfig(self, config_path):
        stream = file(config_path, 'r')
        config = yaml.safe_load(stream)
        for source_path in config.get('source_paths', self.source_paths):
            self.addSourceFolder(source_path)
        self.setBaseIncludeFolder(config.get('base_include_folder', self.include_base_path))
        
        self.default_tier = config.get('default_tier', self.default_tier)
        
        self.tier_step_limit = config.get('tier_reach_limit', None)
        self.setTierStepLimit(self.tier_step_limit)
        
        for module in config.get('modules', []):
            tier = module.get('tier', 1)
            if 'private' == tier:
                tier = -1
            pattern = module.get('pattern', '')
            is_prescient = module.get('prescient', False)
            if isinstance(tier, (int, long)):
                self.addTierForModulesLike(pattern, tier, None, is_prescient)
                
        for module in config.get('third_party_modules', []):
            tier = module.get('tier', 1)
            include_path = module.get('include_path', None)
            if isinstance(tier, (int, long)):
                self.addTierForModulesLike(include_path, tier, include_path)

