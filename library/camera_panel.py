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

        # przechowujemy tylko ostatnią klatkę
        self.latest_frame = None
        self.frame_size = None

        # FPS
        self.frame_counter = 0
        self.last_fps_time = time.time()

        # ---------- UI ----------

        self.connect_button = ctk.CTkButton(
            self,
            text="Connect Camera",
            command=self.connect_camera
        )
        self.connect_button.pack(pady=10)

        self.fps_label = ctk.CTkLabel(self, text="FPS: 0")
        self.fps_label.pack()

        self.image_label = ctk.CTkLabel(
            self,
            text="Camera not connected",
            width=320,
            height=240
        )
        self.image_label.pack(padx=10, pady=10)

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

            # szybka pętla komunikacji z kamerą
            self.after(1, self.camera_loop)

        except Exception as e:
            self.image_label.configure(text=str(e))

    # ------------------------------------------------
    # SCAMP COMMUNICATION LOOP
    # ------------------------------------------------

    def camera_loop(self):

        if not self.running:
            return

        self.camera.update()

        # szybkie odpytywanie kamery
        self.after(1, self.camera_loop)

    # ------------------------------------------------
    # FRAME CALLBACK (very lightweight)
    # ------------------------------------------------

    def on_new_frame(self, buffer, w, h):

        frame = np.frombuffer(buffer, dtype=np.uint8).reshape((h, w))

        # zapisujemy tylko ostatnią klatkę
        self.latest_frame = frame
        self.frame_size = (w, h)

    # ------------------------------------------------
    # GUI UPDATE (slow)
    # ------------------------------------------------

    def gui_update(self):

        if self.latest_frame is not None:

            frame = self.latest_frame

            image = Image.fromarray(frame)

            image = image.resize((320, 240))

            ctk_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=(320, 240)
            )

            self.image_label.configure(image=ctk_image, text="")
            self.image_label.image = ctk_image

            # FPS
            self.frame_counter += 1
            now = time.time()

            if now - self.last_fps_time >= 1:

                fps = self.frame_counter
                self.fps_label.configure(text=f"Display FPS: {fps}")

                self.frame_counter = 0
                self.last_fps_time = now

        # GUI ~30 FPS
        self.after(33, self.gui_update)

    # ------------------------------------------------
    # CLEANUP
    # ------------------------------------------------

    def destroy(self):

        if self.running:
            self.camera.close()

        super().destroy()