import scamp


class ScampCamera:

    def __init__(self):
        self.connected = False
        self.frame_callback = None

    def open_usb(self, device="0"):
        scamp.open_usb(device)
        self.connected = True

    def open_tcp(self, ip="127.0.0.1", port=27888):
        scamp.open_tcp(ip, port)
        self.connected = True

    def update(self):
        """
        Must be called in cycle
        """

        if not self.connected:
            return

        scamp.routine()

        while True:
            packet = scamp.get_packet()

            if packet is None:
                break

            self._process_packet(packet)

    def _process_packet(self, packet):

        if packet['type'] != 'data':
            return

        datatype = packet['datatype']

        if datatype in ["SCAMP5_AOUT", "SCAMP5_DOUT"]:

            w = packet['width']
            h = packet['height']
            buffer = packet['buffer']

            if self.frame_callback:
                self.frame_callback(buffer, w, h)

    def close(self):
        scamp.close()
        self.connected = False