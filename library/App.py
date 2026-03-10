import customtkinter as ctk
from library.tabs import MainTabs
from library.camera_panel import CameraPanel
from library.plot_window import PlotWindow

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.info()

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.camera = CameraPanel(self)
        self.camera.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )
        self.tabs = MainTabs(self)
        self.tabs.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

    def info(self) -> None:
        self.geometry("600x600")
        self.title("SCAMP5 GUI")
        self.resizable(True, True)
    
    def open_plot():
        PlotWindow(self)
    
