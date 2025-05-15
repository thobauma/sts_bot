import time
import logging


from ..communication.communicator import Communicator
from ..sts.gamestate.player import PlayerClass
from ..sts.gamestate.received_state import ReceivedState
from ..sts.gamestate.screen_state import ScreenType
from .base_runner import BaseRunner


class ManualRunner(BaseRunner):
    def climb_spire(self):
        current_state = self.past_states[-1]
        while True:
            if current_state.available_commands:
                self.logger.info(
                    f"available actions: {current_state.available_commands}"
                )
            action = input("Next action: ")

            if not action:
                self.logger.info("No action given. Defaulting to state.")
                action = "state"
            new_state = self.communicator.send_and_receive(action)

            if new_state.error:
                self.logger.info(f"""Error: {new_state.error}""")
                new_state = self.get_current_state()

            current_state = new_state
