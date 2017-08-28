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
        self.mainframe = ttk.Frame(self.root, width=300, height=300)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.mainframe.grid(column=0, row=0, sticky = "NSEW")

        self.hrulercanvas = Canvas(self.mainframe, width=300, borderwidth=0, background="#ffffff")

        self.vrulercanvas = Canvas(self.mainframe, height=300, borderwidth=0, background="#ffffff")
        
        self.deps_canvas = Canvas(self.mainframe, width=300, height=300, borderwidth=0, background="#ffffff")
        self.vscrollbar = ttk.Scrollbar(self.mainframe, orient=VERTICAL)
        self.hscrollbar = ttk.Scrollbar(self.mainframe, orient=HORIZONTAL)
        self.vscrollbar.config(command=self.yview)
        self.hscrollbar.config(command=self.xview)
        self.deps_canvas.config(yscrollcommand=self.vscrollbar.set)
        self.deps_canvas.config(xscrollcommand=self.hscrollbar.set)

        self.hrulercanvas.grid(row=0, column=1, sticky="EW")
        self.vrulercanvas.grid(row=1, column=0, sticky="NS")
        self.deps_canvas.grid(row=1, column=1, sticky="NSEW")
        self.vscrollbar.grid(row=1, column=2, sticky="NS")
        self.hscrollbar.grid(row=2, column=1, sticky="EW")

        self.hrulerframe = ttk.Frame(self.hrulercanvas)
        self.vrulerframe = ttk.Frame(self.vrulercanvas)
        self.hrulerframe.bind("<Configure>", self._onHRulerCanvasConfigure)
        self.vrulerframe.bind("<Configure>", self._onVRulerCanvasConfigure)
        self.hrulerwindow = self.hrulercanvas.create_window(0, 0,
                                                            window=self.hrulerframe,
                                                            anchor="nw",
                                                            tags="self.hrulerframe")
        self.vrulerwindow = self.vrulercanvas.create_window(0, 0,
                                                            window=self.vrulerframe,
                                                            anchor="nw",
                                                            tags="self.vrulerframe")
                
        self.deps_frame = ttk.Frame(self.deps_canvas)
        self.deps_frame.bind("<Configure>", self._onDepsCanvasConfigure)
        self.deps_window = self.deps_canvas.create_window(0, 0,
                                       window=self.deps_frame,
                                       anchor="nw",
                                       tags="self.deps_frame")
        
        self.calculateDependencies()

        ruler_height = 0
        ruler_width = 0
        for item in self.hrulerframe.grid_slaves(row=0):
            ruler_height = max(item.winfo_reqheight(), ruler_height)
        for item in self.vrulerframe.grid_slaves(column=0):
            ruler_width = max(item.winfo_reqwidth(), ruler_width)
        self.hrulercanvas.config(width=300, height=ruler_height)
        self.vrulercanvas.config(width=ruler_width, height=300)
        self.mainframe.columnconfigure(0, weight=0)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.columnconfigure(2, weight=0)
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=0)

    def xview(self, *args):
        apply(self.deps_canvas.xview, args)
        apply(self.hrulercanvas.xview, args)

    def yview(self, *args):
        apply(self.deps_canvas.yview, args)
        apply(self.vrulercanvas.yview, args)

    def _onHRulerCanvasConfigure(self, event):
        self.hrulercanvas.configure(scrollregion=self.hrulerframe.bbox("all"))
        
    def _onVRulerCanvasConfigure(self, event):
        self.vrulercanvas.configure(scrollregion=self.vrulerframe.bbox("all"))
        
    def _onDepsCanvasConfigure(self, event):
        self.deps_canvas.configure(scrollregion=self.deps_frame.bbox("all"))

    def calculateDependencies(self):
        layout = YAMLProjectLayout()
        layout.loadConfig('examples/hangman/.archie-config')

        services = OSProjectServices()

        analyzer = SimpleIncludeDependencyAnalyzer()
        
        resolver = FindIncludeDependencies(layout, services, analyzer)
        
        resolver.findIncludeDependencies('examples/librarymanagement')
        module_names = resolver.getModuleList()
        self._insertColumns(module_names, 1)
        self._insertDependenciesCol(resolver, module_names, module_names, 1)
        self.hrulerframe.rowconfigure(0, weight=1)
        self.vrulerframe.columnconfigure(0, weight=1)
        self._sizeColumns(module_names, 1)

    def _insertColumns(self, module_names, n):
        for module in module_names:
            if isinstance(module, str):
                module_name = str(module)
                ttk.Button(self.hrulerframe, text=module_name).grid(row=0, column=n)
                ttk.Button(self.vrulerframe, text=module_name).grid(row=n, column=0)
                n = n + 1
            else:
                n = self._insertColumns(module.module_list, n)
        return n

    def _insertDependenciesCol(self, resolver, module_names, original_module_names, n1):
        for m1 in module_names:
            if isinstance(m1, str):
                self._insertDependenciesRow(resolver, m1, original_module_names, n1, 1)
                n1 = n1 + 1
            else:
                n1 = self._insertDependenciesCol(resolver, m1.module_list, original_module_names, n1)
        return n1

    def _insertDependenciesRow(self, resolver, m1, module_names, n1, n2):        
        for m2 in module_names:
            if isinstance(m2, str):
                forward_deps = resolver.numDependenciesTo(str(m1), str(m2))
                back_deps = resolver.numDependenciesTo(str(m2), str(m1))
                
                if forward_deps != 0 or back_deps != 0:
                    if forward_deps == 0:
                        bg_color = 'red'
                    elif back_deps == 0:
                        bg_color = 'green'
                    else:
                        bg_color = 'gray'
                    ttk.Label(self.deps_frame, text='1', anchor=CENTER, background=bg_color).grid(row=n1, column=n2, sticky="NSEW")
                n2 = n2 + 1
            else:
                n2 = self._insertDependenciesRow(resolver, m1, m2.module_list, n1, n2)

    def _sizeColumns(self, module_names, n):
        for module in module_names:
            if isinstance(module, str):
                module_name = str(module)
                w = self.hrulerframe.grid_slaves(row=0, column=n)[0].winfo_reqwidth()
                h = self.vrulerframe.grid_slaves(row=n, column=0)[0].winfo_reqheight()
                self.deps_frame.columnconfigure(n, minsize=w)
                self.deps_frame.rowconfigure(n, minsize=h)
                n = n + 1
            else:
                n = self._sizeColumns(module.module_list, n)
        return n
        
def main():
    ui = DependencyUi()
    ui.root.mainloop()
        
if __name__ == "__main__":
    main()
