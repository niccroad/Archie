import unittest

from archie.dependencies.entities.ModuleDependency import TranslationUnit
from archie.dependencies.plugins.SimpleIncludeDependencyAnalyzer import SimpleIncludeDependencyAnalyzer

class TestSimpleIncludeDependencyAnalyzer(unittest.TestCase):
    def test_list_includes(self):
        translation_unit = TranslationUnit(None)
        translation_unit.addSourceFile('archie/dependencies/testdata/SourceFile.cpp')
        translation_unit.addHeaderFile('archie/dependencies/testdata/SourceFile.h')
        
        analyzer = SimpleIncludeDependencyAnalyzer()
        self.assertEquals(['SourceFile.h'], analyzer.listIncludes(translation_unit))
        
    def test_list_multiple_includes(self):
        translation_unit = TranslationUnit(None)
        translation_unit.addSourceFile('archie/dependencies/testdata/MultipleIncludeFile.cpp')
        translation_unit.addHeaderFile('archie/dependencies/testdata/MultipleIncludeFile.h')
        
        analyzer = SimpleIncludeDependencyAnalyzer()
        self.assertEquals(['MultipleIncludeFile.h', 'SourceFile.h'], analyzer.listIncludes(translation_unit))
        
    def test_list_some_system_includes(self):
        translation_unit = TranslationUnit(None)
        translation_unit.addSourceFile('archie/dependencies/testdata/SystemIncludeFile.cpp')
        translation_unit.addHeaderFile('archie/dependencies/testdata/SystemIncludeFile.h')
        
        analyzer = SimpleIncludeDependencyAnalyzer()
        self.assertEquals(['SystemIncludeFile.h', 'QtCore/QFile', 'QtOpenGL/QGLWidget'], analyzer.listIncludes(translation_unit))