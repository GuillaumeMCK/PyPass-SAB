import customtkinter as ctk

GITHUB_URL = "https://github.com/GuillaumeMCK/PyPass-SAB"


class Controllers(ctk.CTkFrame):

    def __init__(self, master=None, about_btn_cmd=None, patch_btn_cmd=None, checkup_btn_cmd=None,
                 **kwargs):
        super().__init__(master=master, border_width=0, **kwargs)
        self.about_btn_cmd = about_btn_cmd
        self.patch_btn_cmd = patch_btn_cmd
        self.checkup_btn_cmd = checkup_btn_cmd
        self.init_widgets()

    def init_widgets(self) -> None:
        # ============ create widgets ============
        self.backup_checkbox = ctk.CTkCheckBox(self, text="Backup")
        self.backup_checkbox.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.about_btn = self._create_btn("About ℹ", self.about_btn_cmd, 0, 0, "e", 5, 5, )
        self.checkup_btn = self._create_btn("Checkup 🔎", self.checkup_btn_cmd, 0, 1, "e", 5, 5)
        self.patch_btn = self._create_btn("Patch 🩹", self.patch_btn_cmd, 0, 2, "e", 5, 5, state="disabled")

        # ============ configure widgets ============
        self.backup_checkbox.select()
        self.columnconfigure(0, weight=1)

    def _create_btn(self, text, command, row, column, sticky, padx, pady, state="normal", width=0) -> ctk.CTkButton:
        btn = ctk.CTkButton(self, text=text, command=command, state=state, width=width)
        btn.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        return btn

    def backup_checkbox_state(self) -> bool:
        """Return True if the user wants to backup the file."""
        return bool(self.backup_checkbox.get())

    def set_patch_btn_state(self, state: str) -> None:
        """Set the patch button state."""
        self.patch_btn.configure(state=state)
