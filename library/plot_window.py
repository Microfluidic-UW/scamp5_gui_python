import customtkinter as ctk
import matplotlib as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PlotWindow(ctk.CTkToplevel):
    
    def __init__(self, master):
        super().__init__(master)

        self.title('PLot')
        self.geometry('400x300')

        self.create_plot()
    
    def create_plot(self):
        
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        fig, ax = plt.subplots()

        ax.plot(x,y)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)