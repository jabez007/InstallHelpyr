from tkinter import *

import TabbedUI
from InstallerTab import InstallerTab
from MonitorTab import MonitorTab


class GUI(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)

        self._init_gui_()

    def _init_gui_(self):
        self.pack(fill=BOTH,
                  expand=True)
        self._interconnect_tabs_()
        self._config_fields_()

    def _config_fields_(self):
        pass

    def _interconnect_tabs_(self):
        container_frame = TabbedUI.TabBar(self,
                                          "Install")
        # Install new instance of Interconnect
        installer_frame = TabbedUI.Tab(self,
                                       "Install")
        InstallerTab(installer_frame)
        container_frame.add(installer_frame)

        # Monitor existing instances of Interconnect
        monitor_frame = TabbedUI.Tab(self,
                                     "Monitor")
        MonitorTab(monitor_frame)
        container_frame.add(monitor_frame)

        container_frame.show()

# # # #
