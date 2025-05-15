import fcntl
import json
import os
import time
from typing import Dict, Any


class Receiver:
    def __init__(self, output_fifo, timeout: float = 50):
        self.output_fifo = open(output_fifo, "r")

        # Reading the pipe does not block if there are no contents
        flag = fcntl.fcntl(self.output_fifo, fcntl.F_GETFD)
        fcntl.fcntl(self.output_fifo, fcntl.F_SETFL, flag | os.O_NONBLOCK)

        self.timeout = timeout
        self.sleep_time = 0.05
        self.num_steps = int(timeout / self.sleep_time)

    def empty_fifo(self) -> None:
        """
        Read and discard all pipe content.

        Typically the caller would do this to ensure that the next message on the fifo
        corresponds to the result of the next action sent to the game.
        """

        self.output_fifo.readlines()


