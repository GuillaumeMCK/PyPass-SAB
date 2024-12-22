import os
import sys
import customtkinter as ctk
from src.widgets.event_viewer import EventViewer

class Controllers(ctk.CTkFrame):

    def __init__(self, master=None, about_btn_cmd=None, patch_btn_cmd=None, checkup_btn_cmd=None, patch_update_btn=None, clear_btn_cmd=None, **kwargs):
        super().__init__(master=master, border_width=0, **kwargs)
        self.ev = EventViewer()  # Initialize EventViewer
        self.about_btn_cmd = about_btn_cmd
        self.patch_btn_cmd = patch_btn_cmd
        self.patch_update_btn = patch_update_btn
        self.checkup_btn_cmd = checkup_btn_cmd
        self.clear_btn_cmd = clear_btn_cmd
        self.init_widgets()

    def init_widgets(self) -> None:
        self.backup_checkbox = ctk.CTkCheckBox(self, text="Backup")
        self.update_checkbox = ctk.CTkCheckBox(self, text="Update", command=self.update_checkbox_callback)

        self.about_btn = self._create_btn(" Restore ", self.about_btn_cmd, 0, 1, "e", 5, 10)
        self.checkup_btn = self._create_btn(" Check ", self.checkup_btn_cmd, 0, 3, "e", 5, 10)
        self.checkup_btn = self._create_btn(" Clear ", self.clear_btn_cmd, 0, 0, "e", 5, 10)
        self.patch_btn = self._create_btn(" Patch ", self.handle_patch_btn_cmd, 0, 2, "e", 5, 10, state="disabled")

        # Add Options Button
        self.options_btn = self._create_btn(" Options ", self.show_options_menu, 0, 4, "e", 5, 10)
        self.columnconfigure(0, weight=1)

    def _create_btn(self, text, command, row, column, sticky, padx, pady, state="normal", width=0) -> ctk.CTkButton:
        btn = ctk.CTkButton(self, text=text, command=command, state=state, width=width)
        btn.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
        return btn

    def show_options_menu(self):
        # Create a new Toplevel window for options
        options_window = ctk.CTkToplevel(self)
        options_window.title("Settings")
        options_window.geometry("530x230")
        options_window.transient(self)  # Make it a modal window
        options_window.grab_set()  # Ensure it stays in the foreground

        # Add Title
        title_label = ctk.CTkLabel(options_window, text="Settings", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=1, columnspan=2, pady=15, sticky="n")

        # Backup Option
        backup_label = ctk.CTkLabel(options_window, text="Enable Backup (recommended)")
        backup_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        backup_checkbox = ctk.CTkCheckBox(options_window, text="", command=lambda: self.toggle_checkbox(self.backup_checkbox))
        backup_checkbox.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        backup_checkbox.select()

        # Update Option
        update_label = ctk.CTkLabel(options_window, text="Disable SABUpdates (172MB)")
        update_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        update_checkbox = ctk.CTkCheckBox(options_window, text="", command=lambda: self.toggle_checkbox(self.update_checkbox))
        update_checkbox.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        update_checkbox.select() if self.update_checkbox_state() else update_checkbox.deselect()

        # Close Button
        close_btn = ctk.CTkButton(options_window, text="Close", command=lambda: self.close_options_menu(options_window))
        close_btn.grid(row=3, column=1, columnspan=2, pady=20)

    def update_checkbox_callback(self):
        """Enable or disable the Patch button based on Update checkbox state."""
        if self.update_checkbox.get():
            self.set_patch_btn_state("normal")
        else:
            self.set_patch_btn_state("disabled")

    def close_options_menu(self, options_window):
        options_window.grab_release()  # Release the modal behavior
        options_window.destroy()

    def toggle_checkbox(self, checkbox):
        if checkbox.get():
            checkbox.deselect()
        else:
            checkbox.select()

    def backup_checkbox_state(self) -> bool:
        return bool(self.backup_checkbox.get())

    def update_checkbox_state(self) -> bool:
        return bool(self.update_checkbox.get())

    def set_patch_btn_state(self, state: str) -> None:
        self.patch_btn.configure(state=state)

    def handle_patch_btn_cmd(self):
        if self.update_checkbox_state():
            self.patch_btn_cmd()
            self.patch_update_btn()
        else:
            self.patch_btn_cmd()

# Example usage
if __name__ == "__main__":
    root = ctk.CTk()
    frame = Controllers(root)
    frame.pack(padx=20, pady=20, fill="both", expand=True)
    root.mainloop()