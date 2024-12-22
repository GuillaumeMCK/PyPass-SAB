import customtkinter as ctk

from src.colors import colors


class EventViewer(ctk.CTkFrame):

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.init_widgets()

    def init_widgets(self) -> None:
        self.text_box = ctk.CTkTextbox(master=self,
                                       font=("Consolas", 13),
                                       corner_radius=0,
                                       fg_color=colors["black"],
                                       wrap="word",
                                       padx=15, pady=5,
                                       state="disabled")
        self.text_box.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.text_box.pack(fill="both", expand=True)
        for color in colors:
            self.text_box.tag_config(color, foreground=colors[color])

    def event(self, event, color="grey", end="") -> None:
        self.text_box.configure(state="normal")
        self.text_box.insert("end", event + end, color)
        self.text_box.yview("moveto", 1)
        self.text_box.configure(state="disabled")

    def event_done(self, msg="Done", end="\n") -> None:
        self.event(msg, "green", end)

    def event_info(self, msg="Info", end="\n") -> None:
        self.event(msg, "yellow", end)

    def event_loading(self, msg="Loading", end="\n") -> None:
        self.event(msg, "pink", end)

    def event_warning(self, msg="Warning", end="\n") -> None:
        self.event(msg, "orange", end)

    def event_error(self, msg="Error", end="\n") -> None:
        self.event(msg, "red", end)

    def add_banner(self, msg="", color="white", end="\n") -> None:
        self.event(msg.center(42, "-"), color, end)

    def clear(self):
        """
        Clear all text in the text box.
        """
        self.text_box.configure(state="normal")  # Permet de modifier la boîte de texte
        self.text_box.delete("1.0", "end")       # Supprime tout le contenu
        self.text_box.configure(state="disabled")  # Réactive l'état "disabled" pour empêcher la modification
        self.add_banner("-")
        self.event_info("            StartAllPatch v0.9.5")
        self.event_info("  This Patch is compatible with SAB 3.x.x.")
        self.add_banner("-")
        self.event("\n")
