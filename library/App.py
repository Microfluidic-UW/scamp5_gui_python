import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.info()
    
    def info(self) -> None:
        self.geometry("1000x1000")
        self.title("SCAMP5 GUI")
        self.resizable(True, True)
    
    def button() -> None:
        pass
