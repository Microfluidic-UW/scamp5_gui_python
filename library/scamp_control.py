import scamp


class ScampControl:

    def set_gui_value(self, index, value):
        scamp.send_gui_value(index, int(value))

    def send_message(self, msg, a=0, b=0):
        scamp.send_message(msg, a, b)