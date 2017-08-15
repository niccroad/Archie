import logging

class HeaderReorganization(object):
    def __init__(self, project_layout, project_services):
        self.project_layout = project_layout
        self.project_services = project_services
    
    def reorganizeHeaders(self):
    	logger = logging.getLogger('Archie')
        logger.debug('Reorganizing source headers into tier folders')
        
        expected_installed_files = dict()
        build_folder_stack = []
        max_tier = 0
        has_prescient_module = self.project_layout.hasPrescientModule()
        build_folder_stack.append(self.project_layout.getSourceFolders())
        while len(build_folder_stack) > 0:
            source_folder_list = build_folder_stack.pop()
            for source_folder in source_folder_list:
                tier = self.project_layout.tierForModule(source_folder)
                max_tier = max(max_tier, tier)
                logger.debug('Source folder %s has default tier %d', source_folder, tier)
                
                source_files = self.project_services.listFiles(source_folder)
                for file_name in source_files:
                    source_file = source_folder + '/' + file_name
                    if self.project_layout.isIncludeFile(source_file):
                        file_tier = self.project_layout.tierForModule(source_file, tier)                        
                        if file_tier == 0 and not has_prescient_module:
                            logger.debug('Include file %s is private', source_file)
                            continue
                        logger.debug('Include file %s has tier %d', source_file, file_tier)
                        max_tier = max(max_tier, file_tier)
                        
                        tier_folder = self.project_layout.getIncludeFolder(file_tier)
                        if not self.project_services.folderExists(tier_folder):
                            self.project_services.createFolder(tier_folder)
                        if tier_folder not in expected_installed_files:
                            expected_installed_files[tier_folder] = set()
                        dest_file = tier_folder + '/' + file_name
                        expected_installed_files[tier_folder].add(dest_file)
                        file_exists = self.project_services.fileExists(dest_file)
                        file_different = not file_exists
                        if file_exists:
                            source_mtime = self.project_services.statFile(source_file)
                            dest_mtime = self.project_services.statFile(dest_file)
                            file_different = source_mtime != dest_mtime
                        if file_different:
                            if file_exists:
                                logger.info('Updating header file %s in tier folder %s as it has changed.', source_file, tier_folder)
                                self.project_services.removeFile(dest_file)
                            else:
                                logger.info('Installing header file %s into tier folder %s as it was missing.', source_file, tier_folder)
                            self.project_services.createLinkedFile(source_file, tier_folder)
                        else:
                            logger.debug('File %s is already installed into tier folder %s', source_file, tier_folder)
                    else:
                        logger.debug('Source file %s is not an include file', source_file)
                        
                build_folder_stack.append(self.project_services.listFolders(source_folder))
        
        # Add any inbetween folders to the header map which were not mentioned by any source directory
        for tier in range(1, max_tier + 1):
            tier_folder = self.project_layout.getIncludeFolder(tier)
            if not self.project_services.folderExists(tier_folder):
                logger.info('Adding empty tier folder %s.', tier_folder)
                self.project_services.createFolder(tier_folder)
            if tier_folder not in expected_installed_files:
                expected_installed_files[tier_folder] = set()
                
        # Remove all the header files we discover in the include folders but not in the source directories 
        for tier_folder, header_file_set in expected_installed_files.items():
            for file_name in self.project_services.listFiles(tier_folder):
                header_file = tier_folder + '/' + file_name
                if not header_file in header_file_set:
                    logger.info('Removing header file %s which has changed tiers or been removed from the source tree.', header_file)
                    self.project_services.removeFile(header_file)