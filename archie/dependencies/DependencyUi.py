from Tkinter import *
from tkFileDialog import *
import ttk, os

from archie.projectmodel.plugins.OSProjectServices import OSProjectServices
from archie.projectmodel.plugins.YAMLProjectLayout import YAMLProjectLayout
from archie.dependencies.plugins.SimpleIncludeDependencyAnalyzer import SimpleIncludeDependencyAnalyzer
from archie.dependencies.behaviours.FindIncludeDependencies import ModuleCollection, FindIncludeDependencies

class HeaderState(object):
    def __init__(self, modules, frame, matrix_labels, ui, layer = 0, horizontal=True):
        self.is_expanded = False
        self.modules = modules
        self.layer = layer
        self.matrix_labels = matrix_labels
        self.ui = ui
        self.buttons = []
        self.sub_header_states = []
        self._addModules(frame,
                         matrix_labels,
                         ui,
                         layer,
                         horizontal,
                         0,
                         modules)
            
    def _addModules(self, frame, matrix_labels, ui, layer, horizontal, item, modules):
        for module in modules:
            if isinstance(module, ModuleCollection):
                if module.is_loop:
                    item = self._addModules(frame,
                                            matrix_labels,
                                            ui,
                                            layer,
                                            horizontal,
                                            item,
                                            module.module_list)
                    continue
                
                sub_state = HeaderState(module.module_list,
                                        frame,
                                        matrix_labels,
                                        ui,
                                        layer + 1,
                                        horizontal)
                self.sub_header_states.append(sub_state)
                
            if horizontal:
                button = ttk.Button(frame,
                                    text=str(module),
                                    command=lambda col=item: self._toggleCol(col))
            else:
                button = ttk.Button(frame,
                                    text=str(module),
                                    command=lambda row=item: self._toggleRow(row))
            self.buttons.append(button)
            item = item + 1
        return item

    def _toggleCol(self, col):
        if col < len(self.sub_header_states):
            self.sub_header_states[col].is_expanded = not self.sub_header_states[col].is_expanded
        grid_col = int(self.buttons[col].grid_info()['column'])
        span_col = self.showColButtons(col, grid_col)
        self.ui.updateContents()
        return span_col

    def _toggleRow(self, row):
        if row < len(self.sub_header_states):
            self.sub_header_states[row].is_expanded = not self.sub_header_states[row].is_expanded
        grid_row = int(self.buttons[row].grid_info()['row'])
        span_row = self.showRowButtons(row, grid_row)
        self.ui.updateContents()
        return span_row

    def showRowButtons(self, row, grid_row):
        span_row = grid_row + 1
        if self.is_expanded:
            for i in range(row, len(self.buttons)):
                if i < len(self.sub_header_states):
                    span_row = self.sub_header_states[i].showRowButtons(0,
                                                                        grid_row)
                else:
                    span_row = grid_row + 1
                self.buttons[i].grid(row=grid_row,
                                     column=self.layer,
                                     rowspan=span_row - grid_row,
                                     sticky="NSEW")
                grid_row = span_row
        else:
            self.hideButtons()
        return span_row        

    def showColButtons(self, col, grid_col):
        span_col = grid_col + 1
        if self.is_expanded:
            for i in range(col, len(self.buttons)):
                if i < len(self.sub_header_states):
                    span_col = self.sub_header_states[i].showColButtons(0,
                                                                        grid_col)
                else:
                    span_col = grid_col + 1
                self.buttons[i].grid(row=self.layer,
                                     column=grid_col,
                                     columnspan=span_col - grid_col,
                                     sticky="NSEW")
                grid_col = span_col
        else:
            self.hideButtons()
        return span_col

    def hideButtons(self):
        for i in range(len(self.buttons)):
            if i < len(self.sub_header_states):
                self.sub_header_states[i].hideButtons()
            self.buttons[i].grid_forget()

    def showColContents(self, col, modules, col_module = None):
        if self.is_expanded:
            for i in range(0, len(modules)):
                module = modules[i]
                if isinstance(module, ModuleCollection):
                    if module.is_loop:
                        self.showColContents(col + i,
                                             module.module_list,
                                             module)
                        continue
                    elif self.sub_header_states[i].is_expanded:
                        self.sub_header_states[i].showColContents(0,
                                                                  module.module_list,
                                                                  module)
                        continue
                info = self.buttons[col + i].grid_info()
                grid_col = int(info['column'])
                colspan = int(info['columnspan'])
                self.ui.showDependencyRow(grid_col, colspan, module)
        else:
            info = self.buttons[col].grid_info()
            grid_col = int(info['column'])
            colspan = int(info['columnspan'])
            self.ui.showDependencyRow(grid_col, colspan, col_module)

    def hideContents(self, modules):
        for i in range(len(modules)):
            module = modules[i]
            if isinstance(module, ModuleCollection):
                if module.is_loop:
                    self.hideContents(module.module_list)
                else:
                    self.sub_header_states[i].hideContents(module.module_list)
            self.ui.hideRowContents(module)        
                
    def showRowContents(self,
                        grid_col,
                        colspan,
                        col_module,
                        col_dict,
                        row,
                        modules,
                        row_module = None):
        if self.is_expanded:
            for i in range(0, len(modules)):
                module = modules[i]
                if isinstance(module, ModuleCollection):
                    if module.is_loop:
                        self.showRowContents(grid_col,
                                             colspan,
                                             col_module,
                                             col_dict,
                                             row + i,
                                             module.module_list,
                                             module)
                        continue
                    elif self.sub_header_states[i].is_expanded:
                        self.sub_header_states[i].showRowContents(grid_col,
                                                                  colspan,
                                                                  col_module,
                                                                  col_dict,
                                                                  0,
                                                                  module.module_list,
                                                                  module)
                        continue
                info = self.buttons[row + i].grid_info()
                grid_row = int(info['row'])
                rowspan = int(info['rowspan'])
                self.ui.showDependencyCell(grid_row, rowspan, module, grid_col, colspan, col_module, col_dict)                
        else:
            info = self.buttons[row].grid_info()
            grid_row = int(info['row'])
            rowspan = int(info['rowspan'])
            self.ui.showDependencyCell(grid_row, rowspan, row_module, grid_col, colspan, col_module, col_dict)
                
class DependencyUi(object):
    def __init__(self):
        self.root = Tk()
        self.root.title("Dependencies")
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.setRootFolder)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)
        
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
        x1,y1,width,height=self.hrulerframe.bbox("all")
        self.hrulercanvas.config(height=height)

        columns = self.hrulerframe.grid_size()[0]
        for c in range(columns):
            x1,y1,width,height = self.hrulerframe.grid_bbox(column=c, row=1)
            self.deps_frame.columnconfigure(c, minsize=width)            
        
    def _onVRulerCanvasConfigure(self, event):
        self.vrulercanvas.configure(scrollregion=self.vrulerframe.bbox("all"))
        x1,y1,width,height=self.vrulerframe.bbox("all")
        self.vrulercanvas.config(width=width)

        rows = self.vrulerframe.grid_size()[1]
        for r in range(rows):
            x1,y1,width,height = self.vrulerframe.grid_bbox(column=1, row=r)
            self.deps_frame.rowconfigure(r, minsize=height)            
        
    def _onDepsCanvasConfigure(self, event):
        self.deps_canvas.configure(scrollregion=self.deps_frame.bbox("all"))

    def setRootFolder(self):
        filename = askopenfilename(initialdir = ".",title = "Select file", filetypes = (("Archie Config","*.archie-config"),("all files","*.*")))
        self.calculateDependencies(filename)
        pass

    def calculateDependencies(self, filename):
        layout = YAMLProjectLayout()
        layout.loadConfig(filename)

        services = OSProjectServices()

        analyzer = SimpleIncludeDependencyAnalyzer()
        
        self.resolver = FindIncludeDependencies(layout, services, analyzer)
        
        self.resolver.findIncludeDependencies(os.path.dirname(filename))
        self.module_names = self.resolver.getModuleList()
        self.matrix_labels = dict()
        self._insertRows(self.module_names)
        self._insertCols(self.module_names)
        self.updateContents()
        self.hrulerframe.rowconfigure(0, weight=1)
        self.hrulerframe.rowconfigure(1, weight=1)
        self.vrulerframe.columnconfigure(0, weight=1)
        self.vrulerframe.columnconfigure(1, weight=1)

    def _insertRows(self, module_names):
        self.row_headers = HeaderState(module_names,
                                       self.vrulerframe,
                                       self.matrix_labels,
                                       self,
                                       0,
                                       False)
        self.row_headers.is_expanded = True
        self.row_headers.showRowButtons(0, 0)
        
    def _insertCols(self, module_names):
        self.col_headers = HeaderState(module_names,
                                       self.hrulerframe,
                                       self.matrix_labels,
                                       self,
                                       0,
                                       True)
        self.col_headers.is_expanded = True
        self.col_headers.showColButtons(0, 0)

    def showDependencyRow(self, grid_col, colspan, col_module):
        if col_module == None:
            return grid_col
        if str(col_module) not in self.matrix_labels:
            self.matrix_labels[str(col_module)] = dict()
        col_dict = self.matrix_labels[str(col_module)]
        self.row_headers.showRowContents(grid_col,
                                         colspan,
                                         col_module,
                                         col_dict,
                                         0,
                                         self.module_names,
                                         None)
        grid_col = grid_col + 1        
        return grid_col

    def updateContents(self):
        self.hideContents()
        self.col_headers.showColContents(0, self.module_names)

    def hideContents(self):
        for m1, col_dict in self.matrix_labels.iteritems():
            for m2, label in col_dict.iteritems():
                label.grid_forget()        

    def hideRowContents(self, col_module):
        if str(col_module) not in self.matrix_labels:
            return
        col_dict = self.matrix_labels[str(col_module)]
        for m, label in col_dict.iteritems():
            label.grid_forget()
            
    def showDependencyCell(self, grid_row, rowspan, row_module, grid_col, colspan, col_module, col_dict):
        if str(row_module) not in col_dict:
            forward_deps = self.resolver.numDependenciesTo(str(row_module),
                                                           str(col_module))
            back_deps = self.resolver.numDependenciesTo(str(col_module),
                                                        str(row_module))                
            if forward_deps != 0 or back_deps != 0:
                text_value = str(max(back_deps, forward_deps))
                if forward_deps == 0:
                    bg_color = 'red'
                elif back_deps == 0:
                    bg_color = 'green'
                else:
                    bg_color = 'gray'

                col_dict[str(row_module)] = ttk.Label(self.deps_frame,
                                                      text=text_value,
                                                      anchor=CENTER,
                                                      background=bg_color)
        if str(row_module) in col_dict:
            entry_label = col_dict[str(row_module)]
            entry_label.grid(row=grid_row,
                             rowspan=rowspan,
                             column=grid_col,
                             columnspan=colspan,
                             sticky="NSEW")
        grid_row = grid_row + 1
        return grid_row
        
def main():
    ui = DependencyUi()
    ui.root.mainloop()
        
if __name__ == "__main__":
    main()
