import customtkinter as ctk
import scamp
import time



class ScampControl(ctk.CTkFrame):

    def __init__(self, master, camera=None):
        super().__init__(master)

        self.last_send_time = {}

        self.camera = camera
        self.params = {}
        row = 0

# ---------- SWITCHES ----------
        self.add_switch("image_output", 1, row); row += 1
        self.add_switch("use_4bit_image_output", 1, row); row += 1

        # ---------- SLIDERS ----------
        self.add_slider("threshold", -127, 127, -55, row); row += 1
        self.add_slider("erosion_iterations", 0, 15, 5, row); row += 1

        self.add_switch("save_bb_data", 1, row); row += 1
        self.add_slider("capture_interval_us", 1, 600, 200, row); row += 1

        # ROI
        self.add_slider("ROI x0", 0, 255, 69, row); row += 1
        self.add_slider("ROI y0", 0, 255, 66, row); row += 1
        self.add_slider("ROI x1", 0, 255, 215, row); row += 1
        self.add_slider("ROI y1", 0, 255, 194, row); row += 1

        # Aspect Ratio
        self.add_slider("Min AR x100", 0, 300, 80, row); row += 1
        self.add_slider("Max AR x100", 0, 300, 120, row); row += 1

        # Playback
        self.add_slider("image index: ", 1, 5000, 1, row); row += 1
        self.add_slider("playback speed", -5, 5, 0, row); row += 1

        # Flags
        self.add_switch("Show ROI", 1, row); row += 1
        self.add_switch("Sort Droplets", 0, row); row += 1

        self.add_slider("High state time", 0, 300, 100, row); row += 1

        self.add_switch("Const voltage", 0, row); row += 1
        self.add_switch("count sorted", 0, row); row += 1

        self.add_slider("sorted_droplets", 0, 10000, 0, row); row += 1
        self.add_slider("all_droplets", 0, 10000, 0, row); row += 1
        print(dir(scamp))

    def send_to_scamp(self, name, value):

        now = time.time()

        if name in self.last_send_time:
            if now - self.last_send_time[name] < 0.05:
                return

        self.last_send_time[name] = now

        if self.camera is None or not self.camera.connected:
            return

        try:
            scamp.send_gui_value(name, int(value))
        except Exception as e:
            print("SCAMP send error:", e)
    
    def add_slider(self, text, from_, to, default, row):

        label = ctk.CTkLabel(self, text=f"{text}: {default}")
        label.grid(row=row, column=0, sticky="w")

        slider = ctk.CTkSlider(self, from_=from_, to=to)
        slider.set(default)
        slider.grid(row=row, column=1, sticky="ew", padx=5)

        def on_change(value):
            value = int(value)

            label.configure(text=f"{text}: {value}")
            self.params[text] = value

            # 🔴 LIVE SYNC
            self.send_to_scamp(text, value)

        slider.configure(command=on_change)

        self.params[text] = default

    def add_switch(self, text, default, row):

        var = ctk.IntVar(value=default)

        switch = ctk.CTkSwitch(
            self,
            text=text,
            variable=var
        )
        switch.grid(row=row, column=0, columnspan=2, sticky="w")

        def on_toggle():
            value = var.get()
            self.params[text] = value

            # 🔴 LIVE SYNC
            self.send_to_scamp(text, value)

        switch.configure(command=on_toggle)

        self.params[text] = default