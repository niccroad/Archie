import unittest

from archie.projectmodel.entities.ProjectLayout import ProjectLayout
from archie.projectmodel.entities.ProjectServices import ProjectServices
from archie.dependencies.behaviours.FindIncludeDependencies import FindIncludeDependencies, ModuleCollection
from archie.dependencies.entities.IncludeDependencyAnalyzer import IncludeDependencyAnalyzer

class StubProjectServices(ProjectServices):
    def __init__(self):
        self.linked_files = dict()
        self.files_lists = dict()
        self.folders_lists = dict()
        self.file_dates = dict()
        self.removed_files = set()
        
    def createLinkedFile(self, source_file, dest_folder):
        self.linked_files[source_file] = dest_folder
        
    def removeFile(self, file_path):
        self.removed_files.add(file_path)
        
    def folderExists(self, folder_path):
        return folder_path in self.folders_lists
    
    def createFolder(self, folder_path):
        self.folders_lists[folder_path] = []
        self.files_lists[folder_path] = []
        
    def statFile(self, file_path):
        return self.file_dates[file_path]
        
    def fileExists(self, file_path):
        return file_path in self.file_dates
    
    def listFiles(self, folder):
        return self.files_lists[folder]
    
    def listFolders(self, folder):
        return self.folders_lists[folder]
        
class StubIncludeDependencyAnalyzer(IncludeDependencyAnalyzer):
    def __init__(self):
        self.include_dependencies = dict()
        
    def listIncludes(self, translation_unit):
        if len(translation_unit.source_files) > 0:
            return self.include_dependencies[translation_unit.source_files[0]]
        elif len(translation_unit.header_files) > 0:
            return self.include_dependencies[translation_unit.header_files[0]]
        else:
            return []

class TestFindIncludeDependencies(unittest.TestCase):
    def test_find_include_dependencies(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Module1'] = ['File1.cpp', 'File1.h', 'File2.h']
        services.files_lists['build/include/T1'] = []
        services.folders_lists['Source'] = ['Source/Module1']
        services.folders_lists['Source/Module1'] = []
        
        analyzer = StubIncludeDependencyAnalyzer()
        analyzer.include_dependencies['Source/Module1/File1.cpp'] = ['File1.h', 'File2.h']
        analyzer.include_dependencies['Source/Module1/File2.h'] = []
        
        resolver = FindIncludeDependencies(layout, services, analyzer)
        
        resolver.findIncludeDependencies()
        self.assertEquals(['Source/Module1/File1.h', 'Source/Module1/File2.h'],
                          resolver.dependenciesOf('Source/Module1/File1.cpp'))

    def test_find_ordered_include_dependencies(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Hangman'] = ['HangmanGame.cpp', 'HangmanGame.h', 'Main.cpp', 'Wordlist_p.h', 'Wordlist_p.cpp']
        services.files_lists['build/include/T1'] = []
        services.folders_lists['Source'] = ['Source/Hangman']
        services.folders_lists['Source/Hangman'] = []
        
        analyzer = StubIncludeDependencyAnalyzer()
        analyzer.include_dependencies['Source/Hangman/Main.cpp'] = ['HangmanGame.h']
        analyzer.include_dependencies['Source/Hangman/HangmanGame.cpp'] = ['HangmanGame.h', 'Wordlist_p.h']
        analyzer.include_dependencies['Source/Hangman/Wordlist_p.cpp'] = ['Wordlist_p.h']
        analyzer.include_dependencies['Source/Hangman/Wordlist_p.h'] = []
        analyzer.include_dependencies['Source/Hangman/HangmanGame.h'] = []
        
        resolver = FindIncludeDependencies(layout, services, analyzer)
        
        resolver.findIncludeDependencies()
        self.assertEquals([['Wordlist_p', 'HangmanGame', 'Main']], resolver.getModuleList())
        self.assertEquals(1, resolver.numDependenciesTo('Main', 'HangmanGame'))
        self.assertEquals(0, resolver.numDependenciesTo('Main', 'Wordlist_p'))
        self.assertEquals(1, resolver.numDependenciesTo('HangmanGame', 'Wordlist_p'))
        self.assertEquals(0, resolver.numDependenciesTo('HangmanGame', 'Main'))

    def test_handle_loops_in_include_dependencies(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Hangman'] = ['HangmanGame.cpp', 'HangmanGame.h', 'Main.cpp', 'Main.h', 'Wordlist_p.h', 'Wordlist_p.cpp']
        services.files_lists['build/include/T1'] = []
        services.folders_lists['Source'] = ['Source/Hangman']
        services.folders_lists['Source/Hangman'] = []
        
        analyzer = StubIncludeDependencyAnalyzer()
        analyzer.include_dependencies['Source/Hangman/Main.cpp'] = ['HangmanGame.h']
        analyzer.include_dependencies['Source/Hangman/HangmanGame.cpp'] = ['Wordlist_p.h']
        analyzer.include_dependencies['Source/Hangman/Wordlist_p.cpp'] = ['Main.h']
        analyzer.include_dependencies['Source/Hangman/Wordlist_p.h'] = []
        analyzer.include_dependencies['Source/Hangman/HangmanGame.h'] = []
        analyzer.include_dependencies['Source/Hangman/Main.h'] = []
        
        resolver = FindIncludeDependencies(layout, services, analyzer)
        
        resolver.findIncludeDependencies()
        self.assertEquals(['(Source/Hangman:3)'], resolver.getModuleList())
        self.assertEquals(1, resolver.numDependenciesTo('Main', 'HangmanGame'))
        self.assertEquals(0, resolver.numDependenciesTo('Main', 'Wordlist_p'))
        self.assertEquals(1, resolver.numDependenciesTo('HangmanGame', 'Wordlist_p'))
        self.assertEquals(0, resolver.numDependenciesTo('HangmanGame', 'Main'))

    def test_handle_sub_component_loops_in_include_dependencies(self):
        layout = ProjectLayout()
        layout.addSourceFolder('Source')
        
        services = StubProjectServices()
        services.files_lists['Source'] = []
        services.files_lists['Source/Hangman'] = ['HangmanGame.cpp', 'HangmanGame.h', 'Main.cpp', 'Wordlist_p.h', 'Wordlist_p.cpp', 'Loop1.h', 'Loop2.h', 'Loop3.h']
        services.files_lists['build/include/T1'] = []
        services.folders_lists['Source'] = ['Source/Hangman']
        services.folders_lists['Source/Hangman'] = []
        
        analyzer = StubIncludeDependencyAnalyzer()
        analyzer.include_dependencies['Source/Hangman/Main.cpp'] = ['HangmanGame.h']
        analyzer.include_dependencies['Source/Hangman/HangmanGame.cpp'] = ['HangmanGame.h', 'Wordlist_p.h']
        analyzer.include_dependencies['Source/Hangman/Wordlist_p.cpp'] = ['Wordlist_p.h', 'Loop1.h']
        analyzer.include_dependencies['Source/Hangman/Wordlist_p.h'] = []
        analyzer.include_dependencies['Source/Hangman/HangmanGame.h'] = []
        analyzer.include_dependencies['Source/Hangman/Loop1.h'] = ['Loop2.h']
        analyzer.include_dependencies['Source/Hangman/Loop2.h'] = ['Loop3.h']
        analyzer.include_dependencies['Source/Hangman/Loop3.h'] = ['Loop1.h']
        
        resolver = FindIncludeDependencies(layout, services, analyzer)
        
        resolver.findIncludeDependencies()
        self.assertEquals([[['Loop1', 'Loop2', 'Loop3'], 'Wordlist_p', 'HangmanGame', 'Main']], resolver.getModuleList())
        self.assertEquals(1, resolver.numDependenciesTo('Main', 'HangmanGame'))
        self.assertEquals(0, resolver.numDependenciesTo('Main', 'Wordlist_p'))
        self.assertEquals(1, resolver.numDependenciesTo('HangmanGame', 'Wordlist_p'))
        self.assertEquals(0, resolver.numDependenciesTo('HangmanGame', 'Main'))        
