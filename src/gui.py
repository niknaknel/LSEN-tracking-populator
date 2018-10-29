# coding=utf-8
import time
import tkMessageBox
import ttk
from Tkinter import *
from tkinterhtml import TkinterHtml
import tkFileDialog
from ttkthemes import themed_tk as tk
from threading import Thread

UBUNTU_ORANGE_100 = "#E95420"
UBUNTU_ORANGE_80 = "#ED764D"
UBUNTU_LIGHT_GREY = "#F5F4F2"
UBUNTU_WARM_GREY_100 = "#AEA79F"
UBUNTU_WARM_GREY_45 = "#DAD7D3"
UBUNTU_COOL_GREY = "#333333"
CANONICAL_AUBERGINE_100 = "#772953"
CANONICAL_AUBERGINE_90 = "#843E64"
GREEN_DARK = "#1F4820"
GREEN_LIGHT = "#2b602c"
RED_CHERRY = "#D33F3F"
RED_CHERRY_LIGHT = "#db4e4e"

WIDTH = 600
HEIGHT = 465
WINDOW_SIZE = (WIDTH, HEIGHT)
SCALE_X = WIDTH/26
SCALE_Y = HEIGHT/17
ICON_SIZE = (48, 48)


class Gui:

    def __init__(self, parent=None):
        self.parent = parent
        self.log = ""
        self.init_style()
        self.init_widgets()

    def show(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()

    def do_nothing(self, event=None):
        return

    def display(self, msg):
        out = "<b>log:</b> " + msg + "<br>"
        self.log += out
        self.displayHTML.reset()
        self.displayHTML.parse("<html>" + self.log + "</html>")

    def init_prog(self):
        self.lblProgress.config(text="Reading CEMIS")
        self.progFrame.tkraise(self.displayHTML)

    def inc_prog(self, msg=""):
        self.progress.step(1)

        if len(msg) > 0:
            self.lblProgress.config(text=msg)

    def set_prog_len(self, num, val=0):
        self.progress.configure(max=num, value=val)

    def complete(self):
        self.lblProgress.config(text="Complete!")
        max = self.progress['max']
        self.progress.config(value=max)
        time.sleep(0.3)
        self.displayHTML.tkraise(self.progFrame)

    def clear(self):
        self.cemis_path = ""
        self.records_dir = ""
        self.track_path = ""
        self.lblSel1.config(text="None selected")
        self.lblSel2.config(text="None selected")
        self.lblSel3.config(text="None selected")
        self.entryName.delete(0, END)
        self.log = ""
        self.displayHTML.parse("")
        self.displayHTML.reset()

    # ---------------------- Reactivity ---------------------------- #

    def choose_cemis_list(self, event=None):
        fpath = tkFileDialog.askopenfilename(initialdir="../data/", title="Select file",
                                               filetypes=(("Text file", "*.txt"),))
        if fpath:
            self.cemis_path = fpath

            lbl = fpath.split('/')[-1]
            if len(lbl) > 32:
                lbl = lbl[:32] + "..."

            self.lblSel1.config(text=lbl)

    def choose_records_dir(self, event=None):
        fpath = tkFileDialog.askdirectory(initialdir="../data/", title="Select folder")
        if fpath:
            self.records_dir = fpath + "/"
            lbl = fpath.split('/')[-1]
            if len(lbl) > 32:
                lbl = lbl[:32] + "..."

            self.lblSel2.config(text=lbl)

    def choose_track_file(self, event=None):
        fpath = tkFileDialog.askopenfilename(initialdir="../data/", title="Select file",
                                             filetypes=(("Excel Workbook", "*.xlsx"),
                                                        ("Excel Workbook (2003-2007)", "*.xls")))
        if fpath:
            self.track_path = fpath
            lbl = fpath.split('/')[-1]
            if len(lbl) > 32:
                lbl = lbl[:32] + "..."

            self.lblSel3.config(text=lbl)

    def submit(self, event=None):
        if self.cemis_path == "" or self.records_dir == "" or self.track_path == "":
            tkMessageBox.showinfo("Alert!", "Please select select all the required files.")
            return

        name = self.entryName.get().strip()

        if len(name) == 0:
            tkMessageBox.showinfo("Alert!", "Please enter the LST.")
            return

        # start process thread
        PROCESS_THREAD = Thread(target=self.parent.process, args=(name, self.cemis_path, self.records_dir, self.track_path))
        PROCESS_THREAD.start()

        self.clear()

# --------------------- GUI instantiation ----------------------- #

    def init_style(self):
        self.root = tk.ThemedTk()
        self.root.get_themes()
        self.root.set_theme("radiance")

        self.root.title("LSEN Tracker")
        self.root.resizable(0, 0)
        self.root.geometry("%dx%d" % WINDOW_SIZE)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.root.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.root.winfo_screenwidth() / 2 - windowWidth)
        positionDown = int(self.root.winfo_screenheight() / 2 - windowHeight)

        # Positions the window in the center of the page.
        self.root.geometry("+{}+{}".format(positionRight, positionDown))
        return

    def init_widgets(self):
        # -- Vars -- #
        self.cemis_path = ""
        self.records_dir = ""
        self.track_path = ""

        # -- Header -- #
        lblHeader = Label(self.root, text="LSEN Tracker", bg=UBUNTU_WARM_GREY_100, fg='white', font=('Ubuntu', 18), relief="groove")
        lblHeader.place(x=0, y=0, width=WIDTH, height=SCALE_Y*2)

        self.init_fc_pane()
        self.init_progress_pane()
        self.init_log_pane()
        return

    def init_fc_pane(self):
        frame = ttk.Frame(self.root, relief="groove")
        frame.place(x=0, y=SCALE_Y*2+2, width=WIDTH, height=SCALE_Y*9.6)

        # -- Labels -- #
        lblFile1 = ttk.Label(frame, text="Choose CEMIS list:")
        lblFile2 = ttk.Label(frame, text="Choose record sheet directory")
        lblFile3 = ttk.Label(frame, text="Choose tracking file:")
        lblFile1.place(x=SCALE_X*3, y=SCALE_Y)
        lblFile2.place(x=SCALE_X*3, y=SCALE_Y*3)
        lblFile3.place(x=SCALE_X*3, y=SCALE_Y*5)

        self.lblSel1 = Label(frame, text="None selected", fg=UBUNTU_WARM_GREY_100, bg=UBUNTU_LIGHT_GREY)
        self.lblSel2 = Label(frame, text="None selected", fg=UBUNTU_WARM_GREY_100, bg=UBUNTU_LIGHT_GREY)
        self.lblSel3 = Label(frame, text="None selected", fg=UBUNTU_WARM_GREY_100, bg=UBUNTU_LIGHT_GREY)
        self.lblSel1.place(x=SCALE_X*3, y=SCALE_Y*1.8)
        self.lblSel2.place(x=SCALE_X*3, y=SCALE_Y * 3.8)
        self.lblSel3.place(x=SCALE_X*3, y=SCALE_Y * 5.8)

        # -- Buttons -- #
        btnSel1 = ttk.Button(frame, text="Open...", command=self.choose_cemis_list)
        btnSel2 = ttk.Button(frame, text="Open...", command=self.choose_records_dir)
        btnSel3 = ttk.Button(frame, text="Open...", command=self.choose_track_file)
        btnSel1.place(x=SCALE_X * 17, y=SCALE_Y + 12)
        btnSel2.place(x=SCALE_X * 17, y=SCALE_Y * 3 + 12)
        btnSel3.place(x=SCALE_X * 17, y=SCALE_Y * 5 + 12)

        btnSubmit = ttk.Button(frame, text="Submit", command=self.submit)
        btnSubmit.place(x=SCALE_X*17, y=SCALE_Y*7.4)

        # -- Entry -- #
        ttk.Label(frame, text="LST: ").place(x=SCALE_X*6+10, y=SCALE_Y*7.5, width=SCALE_X*8, height=SCALE_Y-2)
        self.entryName = ttk.Entry(self.root)
        self.entryName.place(x=SCALE_X*8, y=SCALE_Y*9 + 17, width=SCALE_X*8.5, height=SCALE_Y-2)

    def init_log_pane(self):
        # -- Label -- #
        lblLog = Label(self.root, text="Messages:", bg=UBUNTU_WARM_GREY_100, fg='white', font=('Ubuntu', 14), relief="groove")
        lblLog.place(x=0, y=SCALE_Y * 12-10, width=WIDTH, height=SCALE_Y)

        # -- HTML display -- #
        self.displayHTML = TkinterHtml(self.root)
        self.displayHTML.place(x=0, y=SCALE_Y * 12 + 18, width=WIDTH, height=SCALE_Y * 4.3)
        self.displayHTML.bind('<Button-1>', self.do_nothing)

    def init_progress_pane(self):
        self.progFrame = ttk.Frame(self.root, relief="groove")
        self.progFrame.place(x=0, y=SCALE_Y * 12 + 18, width=WIDTH, height=SCALE_Y * 5.6)

        # -- Progress Bar -- #
        self.progress = ttk.Progressbar(self.progFrame, orient="horizontal", length=SCALE_X * 15, mode="determinate")
        self.progress.place(x=SCALE_X * 5.5, y=SCALE_Y*1.5)

        # -- Label -- #
        self.lblProgress = ttk.Label(self.progFrame, text="Waiting")
        self.lblProgress.config(anchor=CENTER)
        self.lblProgress.place(x=0, y=SCALE_Y*2.5, width=WIDTH)

if __name__ == "__main__":
    Gui().show()