import logging, os, sys

from archie.dependencies.entities.ModuleDependency import ModuleDependency, TranslationUnit

class ModuleCollection(object):
    def __init__(self, name, module_list):
        self.name = "(%s:%d)" % (name, len(module_list))
        self.module_list = module_list

    def append(self, item):
        self.module_list.append(item)

    def __repr__(self):
        return self.name

    def __eq__(self, that):
        return self.module_list.__eq__(that)

class FindIncludeDependencies(object):
    def __init__(self, project_layout, project_services, dependency_analyzer):
        self.project_layout = project_layout
        self.project_services = project_services
        self.dependency_analyzer = dependency_analyzer
        
    def findIncludeDependencies(self, base_path=None):
        logger = logging.getLogger('Archie')
        logger.debug('Analyzing include dependencies')
        
        translation_units = dict()
        # Go through the source, and find all the header and translation unit
        # pairs.
        build_folder_stack = []
        source_folders = self.project_layout.getSourceFolders()
        if base_path != None:
            based_source_folders = []
            for source_folder in source_folders:
                based_source_folders.append(base_path + '/' + source_folder)
            build_folder_stack.append(based_source_folders)
        else:
            build_folder_stack.append(source_folders)
        while len(build_folder_stack) > 0:
            source_folder_list = build_folder_stack.pop()
            for source_folder in source_folder_list:
                source_files = self.project_services.listFiles(source_folder)
                for file_name in source_files:
                    source_file = source_folder + '/' + file_name
                    module_file = self._moduleName(file_name)
                    if not module_file in translation_units:
                        translation_units[module_file] = TranslationUnit(None)
                    if self.project_layout.isIncludeFile(source_file):
                        translation_units[module_file].addHeaderFile(source_file)
                    else:
                        translation_units[module_file].addSourceFile(source_file)
                    
                build_folder_stack.append(self.project_services.listFolders(source_folder))
        #
        self.include_dependencies = dict()
        self.flat_module_list = []
        for module, translation_unit in translation_units.iteritems():
            self.flat_module_list.append(module)
            if module not in self.include_dependencies:
                self.include_dependencies[module] = set()
            
            for include in self.dependency_analyzer.listIncludes(translation_unit):
                module_name = self._moduleName(include)
                if module_name in translation_units:
                    self.include_dependencies[module].add(translation_units[module_name])

        self.tree_module_list = self._topologicalSortModules(self.flat_module_list)
        self.flat_module_list = self._flattenModuleHierarchy(self.tree_module_list)
        self.flat_dependency_count = self._dependencyMatrix(self.flat_module_list)

    # Khan's algorithm for topological sort of a DAG.
    def _topologicalSortModules(self, module_list):
        sorted_list = []
        while len(module_list) > 0:
            num_attempts = len(module_list)
            while num_attempts > 0:
                m1 = module_list.pop(0)
                n2 = None
                for dep in self.include_dependencies[str(m1)]:
                    for h in dep.header_files:
                        try:
                            header_module = self._moduleName(os.path.basename(h))
                            n2 = module_list.index(header_module)
                        except ValueError:
                            pass
                    for s in dep.source_files:
                        try:
                            source_module = self._moduleName(os.path.basename(s))
                            n2 = module_list.index(source_module)
                        except ValueError:
                            pass
                if n2 == None:
                    sorted_list.append(m1)
                    break
                else:
                    module_list.append(m1)
                    num_attempts = num_attempts - 1
                    
            # If we made no progress after num_attempts the graph contains a
            # loop.
            if num_attempts == 0:
                loop_list = self._findLargestLoop(module_list)
                for m in loop_list:
                    module_list.remove(m)
                if len(loop_list) > 0:
                    loop_module = self._loopToModule(loop_list)
                    module_list.append(loop_module)                    
        return sorted_list

    # Floyd-Warshall algorithm for largest path detection
    def _findLargestLoop(self, module_list):
        if len(module_list) <= 1:
            return module_list

        dist = self._distanceMatrix(module_list)

        next_step = []
        for i in range(len(dist)):
            next_step.append([])
            for j in range(len(dist[i])):
                next_step[i].append(j)
        
        # Calculate the shortest distance between nodes
        for k in range(len(module_list)):
            for i in range(len(module_list)):
                for j in range(len(module_list)):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_step[i][j] = next_step[i][k]
                        
        # Find the longest loop in our matrix
        max_i = 0
        max_j = 0
        max_dist = 0
        for i in range(len(dist)):
            if dist[i][i] < sys.maxint and dist[i][i] > max_dist:
                max_dist = dist[i][i]
                max_i = i
                max_j = i

        path_list = []
        while max_dist > 0:
            path_list.append(module_list[max_i])
            max_i = next_step[max_i][max_j]
            max_dist = max_dist - 1
        return path_list

    def _dependencyMatrix(self, module_list):
        dependency_count = []

        n1 = 0
        for m1 in module_list:
            dependency_count.append([])
            for n2 in range(len(module_list)):
                dependency_count[n1].append(0)
                
            for dep in self.include_dependencies[str(m1)]:
                n2 = None
                for h in dep.header_files:
                    try:
                        header_module = self._moduleName(os.path.basename(h))
                        n2 = self.flat_module_list.index(header_module)
                    except ValueError:
                        pass
                for s in dep.source_files:
                    try:
                        source_module = self._moduleName(os.path.basename(s))
                        n2 = self.flat_module_list.index(source_module)
                    except ValueError:
                        pass            
                if n2 != None:
                    dependency_count[n1][n2] = 1
            n1 = n1 + 1

        return dependency_count
    
    def _distanceMatrix(self, module_list):
        dist = self._dependencyMatrix(module_list)
        for i in range(len(dist)):
            for j in range(len(dist[i])):
                if dist[i][j] == 0 or i == j:
                    dist[i][j] = sys.maxint
        return dist

    def _loopToModule(self, loop_list):
        loop_module = ModuleCollection(loop_list[0], loop_list)
        deps = set()
        for m in loop_list:
            deps = deps.union(self.include_dependencies[str(m)])
        self.include_dependencies[str(loop_module)] = deps
        return loop_module

    def _flattenModuleHierarchy(self, module_tree):
        module_list = []
        for m in module_tree:
            module_list.append(str(m))
            if isinstance(m, ModuleCollection):
                module_list += self._flattenModuleHierarchy(m.module_list)
        return module_list
    
    def _moduleName(self, source_path):
        module_name, extension = os.path.splitext(source_path)
        return module_name
        
    def dependenciesOf(self, source_path):
        file_name = os.path.basename(source_path)
        module_name = self._moduleName(file_name)
        if module_name not in self.include_dependencies:
            return []
            
        dependency_list = []    
        for dependency in self.include_dependencies[module_name]:
            dependency_list += dependency.header_files
        return dependency_list

    def getModuleList(self):
        return self.tree_module_list

    def numDependenciesTo(self, module_from, module_to):
        index_from = self.flat_module_list.index(module_from)
        index_to = self.flat_module_list.index(module_to)
        return self.flat_dependency_count[index_from][index_to]
