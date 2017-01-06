from Tkinter import *

import TabbedUI
import InterconnectVersion


class InstallerTab(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)

        self._init_gui_()

    def _init_gui_(self):
        self.pack(fill=BOTH,
                  expand=True)
        self._interconnect_tabs_()

    def _interconnect_tabs_(self):
        container_frame = TabbedUI.TabBar(self,
                                          "Dev")
        # TDE Dev code base
        tde_dev_frame = TabbedUI.Tab(self,
                                     "TDE Dev")
        InterconnectVersion.TdeDev(tde_dev_frame)
        container_frame.add(tde_dev_frame)

        # TDE QA code base
        tde_qa_frame = TabbedUI.Tab(self,
                                    "TDE QA")
        InterconnectVersion.TdeQa(tde_qa_frame)
        container_frame.add(tde_qa_frame)

        # Dev code base
        dev_frame = TabbedUI.Tab(self,
                                 "Dev")
        InterconnectVersion.Dev(dev_frame)
        container_frame.add(dev_frame)

        # Stage 1 code base
        stage1_frame = TabbedUI.Tab(self,
                                    "Stage 1")
        InterconnectVersion.StageOne(stage1_frame)
        container_frame.add(stage1_frame)

        # Stage 2 code base
        stage2_frame = TabbedUI.Tab(self,
                                    "Stage 2")
        InterconnectVersion.StageTwo(stage2_frame)
        container_frame.add(stage2_frame)

        container_frame.show()

# # # #
