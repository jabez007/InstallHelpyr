from Tkinter import *


class MonitorTab(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)

        self._init_gui_()

    def _init_gui_(self):
        self.pack(fill=BOTH,
                  expand=True)
