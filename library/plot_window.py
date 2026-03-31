import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time


class PlotWindow(ctk.CTkToplevel):

    def __init__(self, master):
        super().__init__(master)

        self.title("SCAMP Plots")
        self.geometry("900x700")
        self.running = True

        # -------------------------
        # DATA
        # -------------------------
        self.start_time = time.time()

        self.timestamps = []
        self.all_droplets = []
        self.sorted_droplets = []

        self.histogram = None

        # -------------------------
        # FIGURE
        # -------------------------
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(6, 6))

        # time-series
        self.line_all, = self.ax1.plot([], [], label="All droplets")
        self.line_sorted, = self.ax1.plot([], [], label="Sorted droplets")

        self.ax1.set_title("Droplets over time")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Count")
        self.ax1.legend()

        # histogram
        self.bar_container = None
        self.ax2.set_title("Aspect Ratio Histogram")
        self.ax2.set_xlabel("AR (scaled x100)")
        self.ax2.set_ylabel("Count")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # refresh loop
        self.after(100, self.update_plot)

    # ----------------------------------------
    # CALLBACK FROM SCAMP
    # ----------------------------------------

    def on_scamp_data(self, data):

        # CASE 1: histogram
        if len(data) > 10:
            self.histogram = np.array(data)
            return

        # CASE 2: droplets stats
        if len(data) >= 2:
            t = time.time() - self.start_time

            self.timestamps.append(t)
            self.all_droplets.append(data[0])
            self.sorted_droplets.append(data[1])

    # ----------------------------------------
    # UPDATE PLOT
    # ----------------------------------------

    def update_plot(self):
        if not self.running or not self.winfo_exists():
            return
        # ---- TIME SERIES ----
        if len(self.timestamps) > 0:

            self.line_all.set_data(self.timestamps, self.all_droplets)
            self.line_sorted.set_data(self.timestamps, self.sorted_droplets)

            self.ax1.relim()
            self.ax1.autoscale_view()

        # ---- HISTOGRAM ----
        if self.histogram is not None:

            self.ax2.clear()

            x = np.arange(len(self.histogram))
            self.ax2.bar(x, self.histogram)

            self.ax2.set_title("Aspect Ratio Histogram")
            self.ax2.set_xlabel("AR (scaled x100)")
            self.ax2.set_ylabel("Count")

        self.canvas.draw()
        self.after(100, self.update_plot)

        def destroy(self):
            self.running = False
            super().destroy()