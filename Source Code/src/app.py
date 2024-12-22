import sys
import webbrowser as wb
from os import path
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from Python.Lib import os
from src.colors import colors
from src.patcher import Patcher
from src.update_patcher import UpdatePatcher
from src.widgets import EventViewer, Controllers

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

HEIGHT = 345
WIDTH = 350

GITHUB_URL = "https://github.com/danbenba/StartAllPatch"


class App(ctk.CTk):

    def __init__(self, is_compiled: bool = getattr(sys, 'frozen', False), assets_path="src\\assets" if not getattr(sys, 'frozen', False) else os.path.join(sys._MEIPASS, "assets")):
        super().__init__()
        self.is_compiled = is_compiled
        self.assets_path = "src\\assets" if not self.is_compiled else path.join(sys._MEIPASS, "assets")
        self.icon_path = path.join(self.assets_path, "icon.ico")
        self.iconbitmap(self.icon_path)
        self.setup_widgets()
        self.assets_path = assets_path
        self.patcher = Patcher(self.controllers.backup_checkbox_state, self.event_viewer)
        self.updater = UpdatePatcher(self.controllers.backup_checkbox_state, self.event_viewer)
        self.after(300, self.checkup_btn_cmd)  # wait for the window
        self.patcher.reset_trail_reminder()

    def setup_widgets(self):
        # ============ configure window ============
        self.title("StartAllPatch v0.9.5")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.minsize(WIDTH, HEIGHT)
        self.configure(fg_color=colors["black"], bg_color=colors["white"])

        self.event_viewer = EventViewer(master=self)
        self.event_viewer.grid(row=0, column=0, sticky="nsew")  # sticky="nsew" to stretch vertically and horizontally

        self.controllers = Controllers(self, self.restore_btn_cmd, self.patch_btn_cmd, self.checkup_btn_cmd, self.patch_update_btn, self.clear_btn_cmd)
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
        if not self.patcher.checkup_is_valid:
            # Show a confirmation dialog
            response = messagebox.askyesno(
                "Note",
                "The patch appears to already be applied. Do you still want to proceed?\n\n"
                "If you have enabled the deactivation of SABUpdates, click No to only proceed with disabling SABUpdates.\n\nOr clic on No to cancel."
            )
            if not response:
                return  # Cancel the action
        self.patcher.patch()
        self.patcher.checkup()

    def patch_update_btn(self):
        self.updater.disable_updates(self.assets_path)

    def checkup_btn_cmd(self):
        self.patcher.checkup()
        self._refresh_patch_btn()

    def clear_btn_cmd(self):
        self.updater.ev.clear()

    def _refresh_patch_btn(self):
        if not self.patcher.checkup_is_valid:
            self.controllers.set_patch_btn_state("normal")
        else:
            self.controllers.set_patch_btn_state("normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()
