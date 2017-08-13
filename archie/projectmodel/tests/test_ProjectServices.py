import unittest

from projectmodel.entities.ProjectServices import ProjectServices

class TestProjectServices(unittest.TestCase):
	def test_call_move_header(self):
		services = ProjectServices()
		services.createLinkedFile('Source/Folder1/Entity/File.h', 'Build/include/T1')
		
	def test_list_files(self):
		services = ProjectServices()
		services.listFiles('Source/Folder1')
		
	def test_list_folders(self):
		services = ProjectServices()
		services.listFolders('Source/Folder1')
		