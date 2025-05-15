import logging
import os
import stat
import json
import time
from pathlib import Path
from typing import Dict, Any

from .receiver import Receiver
from .sender import Sender
from ..sts.gamestate.player import PlayerClass
from ..sts.gamestate.received_state import ReceivedState
from ..logging.logger import STSLogger

def init_fifo(filename):
    # Create fifos for communication
    if os.path.exists(filename):
        os.remove(filename)
    print(f"fifo path: {filename}")
    os.mkfifo(filename)
    os.chmod(
        filename,
        stat.S_IRUSR
        | stat.S_IWUSR
        | stat.S_IRGRP
        | stat.S_IWGRP
        | stat.S_IROTH
        | stat.S_IWOTH,
    )


class Communicator:
    def __init__(self, logger: STSLogger, input_path: Path, output_path: Path):
        self.logger = logger
        self.input_path = input_path
        self.output_path = output_path
        init_fifo(self.input_path)
        init_fifo(self.output_path)
        self.receiver: Receiver = Receiver(self.output_path)
        self.sender: Sender = Sender(self.input_path)
    
    def send_ready(self):
        self.logger.info("Send ready")
        self.sender.send_ready()

    def receive_game_state(self) -> Dict[str, Any]:
        """
        Continues reading game state until the game is waiting for action from
        the agent
        """
        for _ in range(self.receiver.num_steps):
            message = self.receiver.output_fifo.readline()
            if len(message) > 0:
                try:
                    state = json.loads(message)
                    if state["ready_for_command"]:
                        return state
                except json.decoder.JSONDecodeError:
                    self.logger.error(
                        "W: Message not in valid JSON, retrying. Contents: " + message
                    )
                    self.receiver.empty_fifo()
                    self.sender.send_state()

            time.sleep(self.receiver.sleep_time)

        raise TimeoutError (
            f"Waited {self.receiver.timeout} seconds for game state to be ready "
            "for command, but it didn't happen."
        )

    def send_and_receive(self, message: str) -> ReceivedState:
        self.logger.info(f"send message: {message}")
        self.receiver.empty_fifo()
        self.sender.send_message(message)
        state = self.receive_game_state()
        if state == {}:
            state = self.current_state()
        self.logger.debug(f"response: {state}")
        return ReceivedState(state_dict=state,**state)

    def start(self, player_class: PlayerClass, ascension: int, seed: str) -> ReceivedState:
        self.receiver.empty_fifo()
        
        while(True):
            state = self.current_state()
            if state.ready_for_command:
                break
        
        msg = f"start {player_class.name} {ascension} {seed}"
        self.logger.debug(f"send message: {msg}")
        self.sender.send_message(msg)
        self.logger.debug("Trying to start")
        tries = 10
        for _ in range(tries):
            state = self.receive_game_state()
            self.logger.debug(f"""available_commands: {state['available_commands']}""")
            if state["in_game"]:
                return ReceivedState(state_dict=state,**state)
            # else:

            time.sleep(0.05)
        
        raise TimeoutError("Waited for game to start, but it didn't happen.")
    
    def current_state(self) -> ReceivedState:
        self.receiver.empty_fifo()
        self.sender.send_state()
        state = self.receive_game_state()
        return ReceivedState(state_dict=state,**state)
    



# class Communicator:
#     def __init__(self, logger: logging.Logger, input_path: Path, output_path: Path):
#         self.logger = logger
#         self.input_path = input_path
#         self.output_path = output_path

#     def setup_fifo(self):
#         init_fifos([self.input_path, self.output_path])
#         self.logger.debug("Opening fifo")
#         self.input_fifo = open(self.input_path, "w")
#         self.logger.debug("Sending Ready")
#         self._send_message("Ready")
#         self.output_fifo = open(self.output_path, "r")
#         flag = fcntl.fcntl(self.output_fifo, fcntl.F_GETFD)
#         fcntl.fcntl(self.output_fifo, fcntl.F_SETFL, flag | os.O_NONBLOCK)
#         self.logger.debug("Opening fifo done")


#     def send_start(self, player_class: PlayerClass, ascension: int, seed: str) -> str:
#        return self.send_and_receive(f"START {player_class} {ascension} {seed}")

    # def send_and_receive(self, message: str) -> str:
    #     self.logger.info(f"send message: {message}")
    #     self.output_fifo.readlines()
    #     self._send_message(message)
    #     response = self.output_fifo.readline()
    #     self.logger.info(f"response: {response}")
    #     return response

#     def _send_message(self, message: str) -> None:
#         self.input_fifo.write(f"{message}\n")
#         self.input_fifo.flush()

