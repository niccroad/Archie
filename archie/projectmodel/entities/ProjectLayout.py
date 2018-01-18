import re

class TierPattern(object):
    def __init__(self, matcher, third_party_path = None, is_prescient = False, priority = 0):
        self.is_third_party = (third_party_path != None)
        self.third_party_path = third_party_path
        self.is_prescient = is_prescient
        self.matcher = matcher
        self.priority = priority

    def _normalizePaths(self, folder_name):
        indexOfColon = folder_name.find(':')
        if indexOfColon != -1:
            folder_name = folder_name[indexOfColon + 1:]
        return folder_name.replace('\\', '/')

    def match(self, folder_name):
        return self.matcher.match(self._normalizePaths(folder_name))

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
        self.tier_step_limit = None
        self.num_tier_patterns = 0

    def getSourceFolders(self):
        return self.source_paths

    def addSourceFolder(self, source_path):
        self.source_paths.append(source_path)

    def setBaseIncludeFolder(self, include_base_path):
        while include_base_path.endswith('/') or include_base_path.endswith('\\'):
            include_base_path = include_base_path[0:-1]
        self.include_base_path = include_base_path

    def setTierStepLimit(self, step_limit):
        if step_limit <= 0:
            step_limit = None
        self.tier_step_limit = step_limit

    def getMinimumReachableTier(self, from_tier):
        if self.tier_step_limit == None:
            return 1
        else:
            return max(1, from_tier - self.tier_step_limit)

    def getIncludeFolder(self, tier):
        self._fillTierFolders(tier)
        return self.include_base_path + '/' + self.tier_folders[tier]

    def getThirdPartyIncludeFolders(self, tier):
    	include_folders = []
    	if len(self.tier_patterns) > tier:
            patterns = self.tier_patterns[tier]
            for pattern in patterns:
        	    if pattern.is_third_party:
        		    include_folders.append(pattern.third_party_path)
    	return include_folders

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

    def addTierForModulesLike(self,
                              pattern,
                              tier,
                              third_party_path = None,
                              is_prescient = False):
        if tier < 0:
            tier = 0
        while (len(self.tier_patterns) <= tier):
            self.tier_patterns.append([])
        matcher = self._convertWildcardsToMatcher(pattern)
        self.num_tier_patterns = self.num_tier_patterns + 1
        tier_pattern = TierPattern(matcher, third_party_path, is_prescient, self.num_tier_patterns)
        self.tier_patterns[tier].append(tier_pattern)

    def _convertWildcardsToMatcher(self, pattern):
        pattern_prefix = ''
        if pattern.startswith('**/'):
            pattern = pattern[3:]
            pattern_prefix = '[\w\s/.-]*'
        pattern_suffix = ''
        if pattern.endswith('/**'):
            pattern = pattern[:-3]
            pattern_suffix = '[\w\s/.-]*'
        replace_dict = {'.':'\.',
                        '/**/':'[\w\s/.-]+',
                        '/**':'[\w\s/.-]+',
                        '**/':'[\w\s/.-]+',
                        '**':'[\w\s/.-]*',
                        '*':'[\w\s.-]+'}
        replace_keys = replace_dict.keys()
        replace_keys = map(lambda x: re.escape(x), replace_keys)
        replace_pattern = re.compile('|'.join(replace_keys))
        pattern = (replace_pattern.sub(lambda x:replace_dict[x.group()],
                                       pattern))

        matcher = re.compile(pattern_prefix + pattern + pattern_suffix + '$')
        return matcher

    def tierForModule(self, folder_name, default_tier = None):
        max_priority = 0
        max_t = None
        for t in range(len(self.tier_patterns)):
            patterns = self.tier_patterns[t]
            for pattern in patterns:
                m = pattern.match(folder_name)
                if m != None and pattern.priority >= max_priority:
                    max_t = t
                    max_priority = pattern.priority
        if max_t != None:
            return max_t
        if default_tier == None:
            default_tier = self.default_tier
        return default_tier

    def isThirdPartyModule(self, folder_name):
        for t in range(len(self.tier_patterns)):
            patterns = self.tier_patterns[t]
            for pattern in patterns:
                m = pattern.match(folder_name)
                if m != None:
                    return pattern.is_third_party
    	return False

    def isPrescientModule(self, folder_name):
        for t in range(len(self.tier_patterns)):
            patterns = self.tier_patterns[t]
            for pattern in patterns:
                m = pattern.match(folder_name)
                if m != None:
                    return pattern.is_prescient
    	return False

    def hasPrescientModule(self):
        for t in range(len(self.tier_patterns)):
            patterns = self.tier_patterns[t]
            for pattern in patterns:
                if pattern.is_prescient:
                    return True
        return False

    def thirdPartyIncludePath(self, folder_name):
        for t in range(len(self.tier_patterns)):
            patterns = self.tier_patterns[t]
            for pattern in patterns:
                m = pattern.match(folder_name)
                if m != None:
                    return pattern.third_party_path
        return None