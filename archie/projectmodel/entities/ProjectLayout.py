import re

class ProjectLayout(object):
    def __init__(self):
        self.source_paths = []
        self.include_base_path = 'build/include'
        self.tier_folders = []
        self.tier_patterns = []
        self.header_matchers = []
        self.header_matchers.append(re.compile('[\w\s]+\.h$'))
        self.header_matchers.append(re.compile('[\w\s]+\.hpp$'))
        self.default_tier = 1
        
    def getSourceFolders(self):
        return self.source_paths
        
    def addSourceFolder(self, source_path):
        self.source_paths.append(source_path)
        
    def setBaseIncludeFolder(self, include_base_path):
        self.include_base_path = include_base_path
        
    def getIncludeFolder(self, tier):
        self._fillTierFolders(tier)
        return self.include_base_path + '/' + self.tier_folders[tier]
        
    def addHeaderPattern(self, pattern):
        matcher = self._convertWildcardsToMatcher(pattern)
        self.header_matchers.append(matcher)
        
    def setDefaultTier(self, tier):
        self.default_tier = tier
        
    def setTierFolder(self, tier, folder_name):
        self._fillTierFolders(tier)
        self.tier_folders[tier] = folder_name
        
    def _fillTierFolders(self, tier):
        t = len(self.tier_folders)
        while (len(self.tier_folders) <= tier):
            self.tier_folders.append('T' + str(t))
            t = t + 1
    
    def isIncludeFile(self, file_path):
        for matcher in self.header_matchers:
            m = matcher.search(file_path)
            if m != None:
                return True
        return False
        
    def addTierForModulesLike(self, pattern, tier):
        if tier < 0:
            tier = 0
        while (len(self.tier_patterns) <= tier):
            self.tier_patterns.append([])
        matcher = self._convertWildcardsToMatcher(pattern)
        self.tier_patterns[tier].append(matcher)
        
    def _convertWildcardsToMatcher(self, pattern):
    	replace_dict = {'.':'\.',
    		            '_':'.',
    		            '**/':'[\w\s/]*',
    		            '**':'[\w\s/]+',
    	                '*':'[\w\s]+'}
    	replace_keys = replace_dict.keys()
    	replace_keys = map(lambda x: re.escape(x), replace_keys)
    	replace_pattern = re.compile('|'.join(replace_keys))
    	pattern = (replace_pattern.sub(lambda x:replace_dict[x.group()], 
    		                           pattern)
    		    + '$')
        matcher = re.compile(pattern)
        return matcher

    def tierForModule(self, folder_name, default_tier = None):
        for t in range(len(self.tier_patterns)):
            patterns = self.tier_patterns[t]
            for pattern in patterns:
                m = pattern.match(folder_name)
                if m != None:
                    return t
        if default_tier == None:
        	default_tier = self.default_tier
        return default_tier