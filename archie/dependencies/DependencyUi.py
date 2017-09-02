from Tkinter import *
import ttk, os

from archie.projectmodel.plugins.OSProjectServices import OSProjectServices
from archie.projectmodel.plugins.YAMLProjectLayout import YAMLProjectLayout
from archie.dependencies.plugins.SimpleIncludeDependencyAnalyzer import SimpleIncludeDependencyAnalyzer
from archie.dependencies.behaviours.FindIncludeDependencies import FindIncludeDependencies

class HeaderState(object):
    def __init__(self, modules, frame, matrix_labels, matrixframe, ui, layer = 0, horizontal=True):
        self.is_expanded = False
        self.modules = modules
        self.layer = layer
        self.matrix_labels = matrix_labels
        self.matrixframe = matrixframe
        self.ui = ui
        self.buttons = []
        self.sub_header_states = []
        self._addModules(frame,
                         matrix_labels,
                         matrixframe,
                         ui,
                         layer,
                         horizontal,
                         0,
                         modules)
            
    def _addModules(self, frame, matrix_labels, matrixframe, ui, layer, horizontal, item, modules):
        for module in modules:
            if not isinstance(module, str):
                if module.is_loop:
                    item = self._addModules(frame,
                                            matrix_labels,
                                            matrixframe,
                                            ui,
                                            layer,
                                            horizontal,
                                            item,
                                            module.module_list)
                    continue
                
                sub_state = HeaderState(module.module_list,
                                        frame,
                                        matrix_labels,
                                        matrixframe,
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
        self.showColContents(col, grid_col, self.modules)
        return span_col

    def _toggleRow(self, row):
        if row < len(self.sub_header_states):
            self.sub_header_states[row].is_expanded = not self.sub_header_states[row].is_expanded
        grid_row = int(self.buttons[row].grid_info()['row'])
        span_row = self.showRowButtons(row, grid_row)
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

    def showColContents(self, col, grid_col, modules, col_module = None):
        if self.is_expanded:
            for i in range(col, len(modules)):
                module = modules[i]
                if not isinstance(module, str):
                    if module.is_loop:
                        grid_col = self.showColContents(0,
                                                        grid_col,
                                                        module.module_list,
                                                        module)
                    else:
                        grid_col = self.sub_header_states[i].showColContents(0,
                                                                             grid_col,
                                                                             module.module_list,
                                                                             module)
                    continue
                grid_col = self.ui.showDependencyRow(grid_col, module)
        else:
            grid_col = self.ui.showDependencyRow(grid_col, col_module)
        return grid_col
                
    def showRowContents(self,
                        grid_col,
                        col_module,
                        col_dict,
                        row,
                        grid_row,
                        modules,
                        row_module = None):
        if self.is_expanded:
            for i in range(row, len(modules)):
                module = modules[i]
                if not isinstance(module, str):
                    if module.is_loop:
                        grid_row = self.showRowContents(grid_col,
                                                        col_module,
                                                        col_dict,
                                                        0,
                                                        grid_row,
                                                        module.module_list,
                                                        module)
                    else:
                        grid_row = self.sub_header_states[i].showRowContents(grid_col,
                                                                             col_module,
                                                                             col_dict,
                                                                             0,
                                                                             grid_row,
                                                                             module.module_list,
                                                                             module)
                    continue
                grid_row = self.ui.showDependencyCell(grid_row, module, grid_col, col_module, col_dict)
                
        else:
            grid_row = self.ui.showDependencyCell(grid_row, row_module, grid_col, col_module, col_dict)
        return grid_row     
                
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

    def calculateDependencies(self):
        layout = YAMLProjectLayout()
        layout.loadConfig('examples/hangman/.archie-config')

        services = OSProjectServices()

        analyzer = SimpleIncludeDependencyAnalyzer()
        
        resolver = FindIncludeDependencies(layout, services, analyzer)
        
        resolver.findIncludeDependencies('examples/librarymanagement')
        self.module_names = resolver.getModuleList()
        self.matrix_labels = dict()
        self._insertRows(self.module_names)
        self._insertCols(self.module_names)
        #self._insertDependenciesCol(resolver, module_names, module_names, 1)
        self.hrulerframe.rowconfigure(0, weight=1)
        self.hrulerframe.rowconfigure(1, weight=1)
        self.vrulerframe.columnconfigure(0, weight=1)
        self.vrulerframe.columnconfigure(1, weight=1)

    def _insertRows(self, module_names):
        self.row_headers = HeaderState(module_names,
                                       self.vrulerframe,
                                       self.matrix_labels,
                                       self.deps_frame,
                                       self,
                                       0,
                                       False)
        self.row_headers.is_expanded = True
        self.row_headers.showRowButtons(0, 0)
        
    def _insertCols(self, module_names):
        self.col_headers = HeaderState(module_names,
                                       self.hrulerframe,
                                       self.matrix_labels,
                                       self.deps_frame,
                                       self,
                                       0,
                                       True)
        self.col_headers.is_expanded = True
        self.col_headers.showColButtons(0, 0)

    def showDependencyRow(self, grid_col, col_module):
        if col_module == None:
            return grid_col
        if str(col_module) not in self.matrix_labels:
            self.matrix_labels[str(col_module)] = dict()
        self.row_headers.showRowContents(grid_col,
                                         col_module,
                                         self.matrix_labels[str(col_module)],
                                         0,
                                         0,
                                         self.module_names,
                                         None)
        grid_col = grid_col + 1        
        return grid_col

    def showDependencyCell(self, grid_row, row_module, grid_col, col_module, col_dict):
        if str(row_module) not in col_dict:
            bg_color = 'red'
            col_dict[str(row_module)] = ttk.Label(self.deps_frame,
                                                  text='1',
                                                  anchor=CENTER,
                                                  background=bg_color)
        entry_label = self.matrix_labels[str(col_module)][str(row_module)]
        entry_label.grid(row=grid_row,
                         column=grid_col,
                         sticky="NSEW")
        grid_row = grid_row + 1
        return grid_row

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
        return n2
        
def main():
    ui = DependencyUi()
    ui.root.mainloop()
        
if __name__ == "__main__":
    main()
