import customtkinter as ctk
from PIL import Image
import numpy as np
import time

from library.scamp_camera import ScampCamera


class CameraPanel(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.camera = ScampCamera()
        self.camera.frame_callback = self.on_new_frame

        self.running = False
        self.frames = {}

        # keep last frame only
        self.latest_frame = None
        self.frame_size = None

        # FPS
        self.frame_counter = 0
        self.last_fps_time = time.time()
        self.last_gui_time = 0

        # ---------- UI ----------

        self.fps_label = ctk.CTkLabel(self, text="FPS: 0")
        self.fps_label.pack()

        # ===== GRID FOR IMAGES =====
        self.image_labels = {}

        titles = {
            0: "1 Captured Image",
            1: "2 Thresholded Image",
            2: "3 Flood Background",
            3: "4 Remove Background",
            4: "5 Erode",
            5: "6 Re-Flood"
        }

        # top panel (pack)
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x")

        self.connect_button = ctk.CTkButton(top_frame, text="Connect Camera", command=self.connect_camera)
        self.connect_button.pack(pady=10)

        # grid panel (grid)
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(fill="both", expand=True)

        self.image_labels = {}
        self.channel_map = {
            101: 0,  # Threshold
            102: 1,  # Flood
            103: 2,  # Remove BG
            104: 3,  # Erode BG
            105: 4,  # Re-flood
        }
        self.next_channel_index = 0
        self.last_rendered = {}
        for ch in range(6):

            row = ch // 3
            col = ch % 3

            frame = ctk.CTkFrame(grid_frame)
            frame.grid(row=row, column=col, padx=5, pady=5)

            label_title = ctk.CTkLabel(frame, text=titles.get(ch, f"Channel {ch}"))
            label_title.pack()

            label_img = ctk.CTkLabel(frame, text="", width=200, height=150)
            label_img.pack()

            self.image_labels[ch] = label_img

            # GUI refresh ~30 FPS
        self.after(33, self.gui_update)

    # ------------------------------------------------
    # CAMERA CONNECT
    # ------------------------------------------------

    def connect_camera(self):

        if self.running:
            return

        try:
            self.camera.open_usb()

            self.running = True
            self.connect_button.configure(
                text="Connected",
                state="disabled"
            )

            self.after(1, self.camera_loop)

        except Exception as e:
            self.image_label.configure(text=str(e))

        else:
            self.camera.open_tcp("127.0.0.1", 27888)
    # ------------------------------------------------
    # SCAMP COMMUNICATION LOOP
    # ------------------------------------------------


    def camera_loop(self):

        if not self.running or not self.winfo_exists():
            return

        self.camera.update()
        self.after(1, self.camera_loop)

    # ------------------------------------------------
    # FRAME CALLBACK
    # ------------------------------------------------

    def on_new_frame(self, buffer, w, h, channel):

        # dynamic mapping
        if channel not in self.channel_map:

            if self.next_channel_index < 6:
                self.channel_map[channel] = self.next_channel_index
                self.next_channel_index += 1

            else:
                return
        print("CHANNEL:", channel)
        mapped_ch = self.channel_map[channel]

        frame = np.frombuffer(buffer, dtype=np.uint8).reshape((h, w))

        self.frames[mapped_ch] = frame


    def gui_update(self):

        now = time.time()
        if not self.winfo_exists():
            return
        # max 30 FPS
        if now - self.last_gui_time < 1/30:
            self.after(5, self.gui_update)
            return

        self.last_gui_time = now

        for ch, frame in self.frames.items():

            if ch not in self.image_labels:
                continue

            image = Image.fromarray(frame)
            image = image.resize((200, 150), Image.NEAREST)

            ctk_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(200, 150)
            )

            label = self.image_labels[ch]
            label.configure(image=ctk_image, text="")
            label.image = ctk_image

        self.after(5, self.gui_update)

    def destroy(self):

        self.running = False

        if self.camera:
            self.camera.close()

        super().destroy()