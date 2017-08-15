import logging

class IncludePath(object):
    def __init__(self, project_layout, project_services):
        self.project_layout = project_layout
        self.project_services = project_services

    def resolveIncludePaths(self,
    	                    folder_path,
    	                    include_third_party = True,
    	                    include_tiers = True):
        logger = logging.getLogger('Archie')
        logger.debug('List include folders for path %s', folder_path)       

        tier = self.project_layout.tierForModule(folder_path)
        logger.debug('Folder path %s has tier %d', folder_path, tier)

        paths = []
        if include_third_party:
            for t in range(1, tier + 1):
                third_party_paths = self.project_layout.getThirdPartyIncludeFolders(t)
                for third_party_folder in third_party_paths:
            	    logger.debug('Tier %d third party folder %s is included', t, third_party_folder)
                paths += third_party_paths

        if include_tiers:
            source_folders = self.project_services.listFolders(folder_path)
            for source_folder in source_folders:
                folder_tier = self.project_layout.tierForModule(source_folder)
                if folder_tier == 0:
                    logger.debug('Private module %s is included', source_folder)
                    paths.append(source_folder)
        
            for t in range(1, tier + 1):
                tier_folder =self.project_layout.getIncludeFolder(t)
                logger.debug('Tier %d folder %s is included', t, tier_folder)
                paths.append(tier_folder)
            
        return paths
