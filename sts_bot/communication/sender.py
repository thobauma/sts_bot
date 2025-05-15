class Sender:
    def __init__(self, input_fifo):
        self.input_fifo = open(input_fifo, "w")

    def _send_message(self, msg: str) -> None:
        self.input_fifo.write(f"{msg}\n")
        self.input_fifo.flush()

    def send_message(self, msg: str) -> None:
        self._send_message(msg)

    def send_ready(self) -> None:
        self._send_message("ready")

    def send_state(self) -> None:
        self._send_message("state")
