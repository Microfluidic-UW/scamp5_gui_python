import customtkinter as ctk
from library.camera_panel import CameraPanel
from library.plot_window import PlotWindow
from library.scamp_control import ScampControl


class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.info()

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.camera = CameraPanel(self)
        self.camera.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.control = ScampControl(self)
        self.control.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        # przycisk do otwarcia plotów
        self.plot_button = ctk.CTkButton(
            self.control,
            text="Open Plots",
            command=self.open_plot
        )
        self.plot_button.grid(row=999, column=0, columnspan=2, pady=10)

        self.plot_window = None
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def info(self):
        self.geometry("1200x1000")
        self.title("SCAMP5 GUI")
        self.resizable(True, True)

    def open_plot(self):

        if self.plot_window is None or not self.plot_window.winfo_exists():
            self.plot_window = PlotWindow(self)

            # 🔴 KLUCZOWE POŁĄCZENIE
            self.camera.camera.data_callback = self.plot_window.on_scamp_data
    
    def on_close(self):

        if hasattr(self, "camera"):
            self.camera.destroy()

        if hasattr(self, "plot_window") and self.plot_window:
            if self.plot_window.winfo_exists():
                self.plot_window.destroy()

        self.destroy()