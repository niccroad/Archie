class TranslationUnit(object):
	def __init__(self, header_file, source_file = None):
		self.header_files = []
		self.source_files = []
		
	def addHeaderFile(self, header_file):
		self.header_files.append(header_file)
		
	def addSourceFile(self, source_file):
		self.source_files.append(source_file)

class ModuleDependency(object):
	def __init__(self, source_unit, included_unit):
		self.source_unit = source_unit
		self.included_unit = included_unit