import os, subprocess

from archie.projectmodel.entities.ProjectServices import ProjectServices

class OSProjectServices(ProjectServices):
    def __init__(self):
        self.devnull = open(os.devnull, 'w')
    
    def createLinkedFile(self, source_file, dest_folder):
        if dest_folder.endswith('/'):
            dest_folder = dest_folder[:-1]
        folder, filename = os.path.split(source_file)
        if not os.path.exists(dest_folder + '/' + filename):
            self._makeLink(source_file, dest_folder, filename)
                
    def _makeLink(self, source_file, dest_folder, filename):
        try:
            os.link(source_file, os.path.join(dest_folder, filename))
        except AttributeError:
            subprocess.call('MKLINK /H %s %s' % (filename, os.path.abspath(source_file)),
                            shell = True,
                            stdout = self.devnull,
                            cwd = dest_folder)
            
    def removeFile(self, file_path):
        os.unlink(file_path)
        
    def fileExists(self, file_path):
        return os.path.isfile(file_path)
        
    def statFile(self, file_path):
        file_stat = os.stat(file_path)
        if file_stat != None:
            return file_stat.st_mtime
        return None;
        
    def folderExists(self, folder_path):
        return os.path.isdir(folder_path)
    
    def createFolder(self, folder_path):
        os.makedirs(folder_path)
    
    def listFiles(self, folder):
        if folder.endswith('/'):
            folder = folder[:-1]
        files = []
        for f in os.listdir(folder):
            full_path = folder + '/' + f
            if os.path.isfile(full_path):
                files.append(f)
        return files
    
    def listFolders(self, folder):
        if folder.endswith('/'):
            folder = folder[:-1]
        folders = []
        for f in os.listdir(folder):
            full_path = folder + '/' + f
            if not os.path.isfile(full_path):
                folders.append(full_path)
        return folders
