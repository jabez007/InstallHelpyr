from tkinter import *
import tkMessageBox
import os

import Setup


class InterconnectVersion(Frame):

    def __init__(self, master=None, cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)

        self.bokrug_root = r"\\bokrug\Builds\Interconnect"
        self.interconnects = ["ce-ic{num:02d}".format(num=ic) for ic in range(1, 11)]
        self.interconnect_root = r"C:\Interconnect"
        self.reverse_proxies = ["ce-proxy", "ce-proxy02"]
        self.msi = ""

        self.codebase = None
        self.ic_server = None
        self.rp_server = None
        self.cache_server = None
        self.cache_port = None

    def _init_gui_(self, title):
        self.pack(fill=BOTH,
                  expand=True)

        config_frame = self._create_frame_(self, side=TOP)
        self._codebase_(config_frame, title)
        self._interconnect_server_(config_frame)
        self._reverse_proxy_(config_frame)
        self._cache_connections_(config_frame)

        button_frame = self._create_frame_(self, side=TOP)
        self._setup_button_(button_frame)

    def _setup_button_(self, frame, **kw):
        setup_button = Button(frame,
                              text="Install",
                              command=self._on_setup_)
        setup_button.pack(**kw)

    def _cache_connections_(self, frame):
        cache_frame = self._create_frame_(frame, side=LEFT)
        self._create_label_(cache_frame, "Cache Server")
        self.cache_server = self._create_entry_(cache_frame)
        self._create_label_(cache_frame, "Cache Port")
        self.cache_port = self._create_entry_(cache_frame)

    def _reverse_proxy_(self, frame):
        reverse_proxy_frame = self._create_frame_(frame, side=LEFT)
        self._create_label_(reverse_proxy_frame, "Reverse Proxy server")
        self.rp_server = self._create_listbox_(reverse_proxy_frame)
        self._fill_listbox_(self.rp_server, self.reverse_proxies)

    def _interconnect_server_(self, frame):
        interconnect_frame = self._create_frame_(frame, side=LEFT)
        self._create_label_(interconnect_frame, "Interconnect server")
        self.ic_server = self._create_listbox_(interconnect_frame)
        self._fill_listbox_(self.ic_server, self.interconnects)
        self._create_label_(interconnect_frame, "Interconnect IIS Directory")
        self.iis_directory = self._create_entry_(interconnect_frame)

    def _codebase_(self, frame, title):
        listbox_frame = self._create_frame_(frame, side=LEFT)
        self._create_label_(listbox_frame,
                            title)
        self.codebase = self._create_listbox_(listbox_frame)
        self._fill_codebase_()

    def _fill_codebase_(self):
        for f in os.listdir(self.bokrug_root):
            if f.upper().endswith("%s-MSI" % self.msi.upper()):
                self.codebase.insert(END, f)

    def _on_setup_(self):
        try:
            codebase = self._get_listbox_selection_(self.codebase)
            interconnect_server = self._get_listbox_selection_(self.ic_server)
            reverse_proxy_server = self._get_listbox_selection_(self.rp_server)
        except TclError:
            tkMessageBox.showerror(title="Installer Error",
                                   message="Missing required selection")
            return

        instance_name = self.iis_directory.get()
        if not instance_name:
            tkMessageBox.showerror(title="Installer Error",
                                   message="Missing IIS directory for new instance")
            return

        cache_server = self.cache_server.get()
        if not cache_server:
            tkMessageBox.showerror(title="Installer Error",
                                   message="Missing Cache server to connect to")
            return

        cache_port = self.cache_port.get()
        if not cache_port.isdigit():
            tkMessageBox.showerror(title="Installer Error",
                                   message="The Cache port you entered is not a number")
            return

        Setup.main(self.bokrug_root, codebase, interconnect_server,
                   self.interconnect_root, instance_name, reverse_proxy_server)

    @staticmethod
    def _get_listbox_selection_(listbox):
        return listbox.get(listbox.curselection())

    @staticmethod
    def _create_frame_(frame, **kw):
        frame = Frame(frame)
        frame.pack(**kw)
        return frame

    @staticmethod
    def _create_label_(frame, title, **kw):
        label = Label(frame, text=title)
        label.pack(**kw)

    @staticmethod
    def _create_listbox_(frame, **kw):
        listbox = Listbox(frame,
                          exportselection=False)
        listbox.pack(**kw)
        return listbox

    @staticmethod
    def _fill_listbox_(listbox, array):
        for i in array:
            listbox.insert(END, i)

    @staticmethod
    def _create_entry_(frame, **kw):
        entry = Entry(frame)
        entry.pack(**kw)
        return entry

# # # #


class Dev(InterconnectVersion):

    def __init__(self, master=None, cnf={}, **kw):
        InterconnectVersion.__init__(self, master, cnf, **kw)

        self.msi = "Dev"

        self._init_gui_("Dev")

    def _fill_codebase_(self):
        for f in os.listdir(self.bokrug_root):
            if f.upper().endswith("%s" % self.msi.upper()):
                self.codebase.insert(END, f)

# # # #


class StageOne(InterconnectVersion):

    def __init__(self, master=None, cnf={}, **kw):
        InterconnectVersion.__init__(self, master, cnf, **kw)

        self.msi = "Stage1"

        self._init_gui_("Stage 1")

# # # #


class StageTwo(InterconnectVersion):

    def __init__(self, master=None, cnf={}, **kw):
        InterconnectVersion.__init__(self, master, cnf, **kw)

        self.msi = "Stage2"

        self._init_gui_("Stage 2")

# # # #


class Tde(InterconnectVersion):

    def __init__(self, master=None, cnf={}, **kw):
        InterconnectVersion.__init__(self, master, cnf, **kw)

        self.bokrug_root = r"\\epic-nfs\nfs_ask\interconnect\Builds\TDE-IC"

    def _fill_codebase_(self):
        for f in os.listdir(self.bokrug_root):
            if f.upper().endswith("%s" % self.msi.upper()):
                self.codebase.insert(END, f)

# # # #


class TdeDev(Tde):

    def __init__(self, master=None, cnf={}, **kw):
        Tde.__init__(self, master, cnf, **kw)

        self.msi = "Dev"
        self.interconnects = ["ce-dev-tde"]

        self._init_gui_("TDE Dev")

# # # #


class TdeQa(Tde):

    def __init__(self, master=None, cnf={}, **kw):
        Tde.__init__(self, master, cnf, **kw)

        self.msi = "QA"
        self.interconnects = ["ce-qa-tde"]

        self._init_gui_("TDE QA")

# # # #
