import logging

class IncludePath(object):
    def __init__(self, project_layout, project_services):
        self.project_layout = project_layout
        self.project_services = project_services

    def resolveIncludePaths(self, folder_path):
        logger = logging.getLogger('Archie')
        logger.debug('List include folders for path %s', folder_path)       

        paths = []

        source_folders = self.project_services.listFolders(folder_path)
        for source_folder in source_folders:
            tier = self.project_layout.tierForModule(source_folder)
            if tier == 0:
                logger.debug('Private module %s is included', source_folder)
                paths.append(source_folder)
        
        tier = self.project_layout.tierForModule(folder_path)
        logger.debug('Folder path %s has tier %d', folder_path, tier)
        for t in range(1, tier + 1):
            logger.debug('Tier %d folder %s is included', t, source_folder)
            paths.append(self.project_layout.getIncludeFolder(t))
            
        return paths
