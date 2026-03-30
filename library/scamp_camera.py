import scamp


class ScampCamera:

    def __init__(self):
        self.connected = False
        self.frame_callback = None
        self.data_callback = None

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

        if packet['datatype'] in ["SCAMP5_AOUT", "SCAMP5_DOUT"]:

            if 'buffer' not in packet:
                return

            w = packet['width']
            h = packet['height']
            buffer = packet['buffer']
            channel = packet.get('channel', 0)

            if self.frame_callback:
                self.frame_callback(buffer, w, h, channel)
        elif packet['datatype'] == 'VS_POST_INT32':

            data = packet.get('data', [])

            if hasattr(self, "data_callback") and self.data_callback:
                self.data_callback(data)

    def close(self):
        scamp.close()
        self.connected = False