import sys
import webbrowser as wb
from os import path

import customtkinter as ctk
from PIL import Image

from src.colors import colors
from src.patcher import Patcher
from src.widgets import EventViewer, Controllers

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HEIGHT = 330
WIDTH = 350

GITHUB_URL = "https://github.com/GuillaumeMCK/PyPass-SAB"


class App(ctk.CTk):

    def __init__(self, is_compiled: bool = getattr(sys, 'frozen', False)):
        super().__init__()
        self.is_compiled = is_compiled
        self.assets_path = "src\\assets" if not self.is_compiled else path.join(sys._MEIPASS, "assets")
        self.icon_path = path.join(self.assets_path, "icon.ico")
        self.iconbitmap(self.icon_path)
        self.setup_widgets()
        self.patcher = Patcher(self.controllers.backup_checkbox_state, self.event_viewer)
        self.after(300, self.checkup_btn_cmd)  # wait for the window
        self.patcher.reset_trail_reminder()

    def setup_widgets(self):
        # ============ configure window ============
        self.title("PyPass-SAB")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)
        self.configure(fg_color=colors["black"], bg_color=colors["white"])

        self.event_viewer = EventViewer(master=self)
        self.event_viewer.grid(row=0, column=0, sticky="nsew")  # sticky="nsew" to stretch vertically and horizontally

        self.controllers = Controllers(self, self.restore_btn_cmd, self.patch_btn_cmd, self.checkup_btn_cmd)
        self.controllers.grid(row=1, column=0, sticky="we", padx=10, pady=10)  # sticky="we" to stretch horizontally

        gh_logo = ctk.CTkImage(dark_image=Image.open(path.join(self.assets_path, "github.png")))
        self.gh_button = ctk.CTkButton(self, text="", image=gh_logo, command=self.about_btn_cmd, width=32,
                                       height=32, fg_color=colors["black"])
        self.gh_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

        # ============ configure grid ============
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)

    def about_btn_cmd(self):
        wb.open(GITHUB_URL)

    def restore_btn_cmd(self):
        self.patcher.restore()

    def patch_btn_cmd(self):
        self.patcher.patch()
        self.patcher.checkup()

    def checkup_btn_cmd(self):
        self.patcher.checkup()
        self._refresh_patch_btn()

    def _refresh_patch_btn(self):
        if not self.patcher.checkup_is_valid:
            self.controllers.set_patch_btn_state("disabled")
        else:
            self.controllers.set_patch_btn_state("normal")
