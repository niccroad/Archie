import re

from archie.dependencies.entities.IncludeDependencyAnalyzer import IncludeDependencyAnalyzer
from archie.dependencies.entities.ModuleDependency import TranslationUnit

class SimpleIncludeDependencyAnalyzer(IncludeDependencyAnalyzer):
    def __init__(self):
        self.include_regex = re.compile('#include\s*[<"](.+)[">]')
        
    def listIncludes(self, translation_unit):
        includes = []
        for source_file in translation_unit.source_files:
            includes += self._listIncludes(source_file)
        for header_file in translation_unit.header_files:
            includes += self._listIncludes(header_file)
        return includes
        
    def _listIncludes(self, source_file):
        includes = []
        for i, line in enumerate(open(source_file)):
            for match in re.finditer(self.include_regex, line):
                includes.append(match.group(1))
        return includes