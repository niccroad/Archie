from Tkinter import *
import ttk, os

from archie.projectmodel.plugins.OSProjectServices import OSProjectServices
from archie.projectmodel.plugins.YAMLProjectLayout import YAMLProjectLayout
from archie.dependencies.plugins.SimpleIncludeDependencyAnalyzer import SimpleIncludeDependencyAnalyzer
from archie.dependencies.behaviours.FindIncludeDependencies import FindIncludeDependencies

class DependencyUi(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Dependencies")
        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
        self.mainframe.columnconfigure(0, weight = 1)
        self.mainframe.rowconfigure(0, weight = 1)
        
        self.calculateDependencies()

    def calculateDependencies(self):
        layout = YAMLProjectLayout()
        layout.loadConfig('examples/hangman/.archie-config')

        services = OSProjectServices()

        analyzer = SimpleIncludeDependencyAnalyzer()
        
        resolver = FindIncludeDependencies(layout, services, analyzer)
        
        resolver.findIncludeDependencies('examples/librarymanagement')
        module_names = resolver.getModuleList()
        n = 1
        for module_name in module_names:
            ttk.Button(self.mainframe, text=module_name).grid(row=0, column=n)
            ttk.Button(self.mainframe, text=module_name).grid(row=n, column=0)
            n = n + 1

        n1 = 1
        for m1 in module_names:
            n2 = 1
            for m2 in module_names:
                forward_deps = resolver.numDependenciesTo(m1, m2)
                back_deps = resolver.numDependenciesTo(m2, m1)
                
                if forward_deps != 0 or back_deps != 0:
                    if forward_deps == 0:
                        bg_color = 'red'
                    elif back_deps == 0:
                        bg_color = 'green'
                    else:
                        bg_color = 'gray'
                    ttk.Label(self.mainframe, text='1', background=bg_color).grid(row=n1, column=n2)                
                n2 = n2 + 1
            n1 = n1 + 1
                    
def main():
    ui = DependencyUi()
    ui.root.mainloop()
        
if __name__ == "__main__":
    main()
