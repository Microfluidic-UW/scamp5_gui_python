import customtkinter as ctk


class MainTabs(ctk.CTkTabview):

    def __init__(self, master):
        super().__init__(master)

        self.add("Analysis")
        self.add("Settings")

        self.create_analysis_tab()
        self.create_settings_tab()

    def create_analysis_tab(self):

        label = ctk.CTkLabel(
            self.tab("Analysis"),
            text="Analysis tools"
        )
        label.pack(pady=20)

    def create_settings_tab(self):

        label = ctk.CTkLabel(
            self.tab("Settings"),
            text="Settings"
        )
        label.pack(pady=20)