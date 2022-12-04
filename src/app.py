import customtkinter as ctk
import webbrowser as wb

from src.widgets import EventViewer, Controllers
from src.colors import colors
from src.patcher import Patcher

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HEIGHT = 320
WIDTH = 350

GITHUB_URL = "https://github.com/GuillaumeMCK/PyPass-SAB"


class App(ctk.CTk):

    def __init__(self, is_compiled: bool = False):
        super().__init__()
        self.is_compiled = is_compiled
        self.setup_widgets()
        self.patcher = Patcher(self.controllers.backup_checkbox_state, self.event_viewer)
        self.checkup_btn_cmd()

    def setup_widgets(self):
        # ============ configure window ============
        self.title("PyPass-SAB")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)
        self.configure(fg_color=colors["black"], bg_color=colors["white"])

        self.event_viewer = EventViewer(master=self)
        self.event_viewer.grid(row=0, column=0, sticky="nsew")

        self.controllers = Controllers(self, self.about_btn_cmd, self.patch_btn_cmd, self.checkup_btn_cmd)
        self.controllers.grid(row=1, column=0, sticky="we", padx=10, pady=10)  # sticky="we" to stretch horizontally

        # ============ configure grid ============
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)

    def about_btn_cmd(self):
        wb.open(GITHUB_URL)

    def patch_btn_cmd(self):
        self.patcher.patch()

    def checkup_btn_cmd(self):
        self.patcher.checkup()
        self._refresh_patch_btn()

    def _refresh_patch_btn(self):
        if not self.patcher.checkup_is_valid:
            self.controllers.set_patch_btn_state("disabled")
        else:
            self.controllers.set_patch_btn_state("normal")
