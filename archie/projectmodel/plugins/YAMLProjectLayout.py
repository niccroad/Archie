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
        for module in config.get('modules', []):
            tier = module.get('tier', 1)
            if 'private' == tier:
                tier = -1
            pattern = module.get('pattern', '')
            if isinstance(tier, (int, long)):
                self.addTierForModulesLike(pattern, tier)
                
        for module in config.get('third_party_modules', []):
            tier = module.get('tier', 1)
            include_path = module.get('include_path', None)
            if isinstance(tier, (int, long)):
                self.addTierForModulesLike(include_path, tier, include_path)

