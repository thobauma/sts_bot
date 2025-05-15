import time

from sts_bot.agent.agent import Agent

# from ..communication.communicator import Communicator
from ..sts.gamestate.player import PlayerClass

# from ..sts.gamestate.received_state import ReceivedState
from ..sts.gamestate.screen_state import ScreenType
from .base_runner import BaseRunner


class AgenticRunner(BaseRunner):
    def __init__(self, agent: Agent, **kwargs):
        super().__init__(**kwargs)
        self.agent = agent

    def climb_spire(self):
        current_state = self.past_states[-1]
        while True:
            action = self.agent.get_next_action(current_state)

            new_state = self.communicator.send_and_receive(action)

            if new_state.error:
                self.logger.info(f"""Error: {new_state.error}""")
                new_state = self.get_current_state()
            current_state = new_state
            # self.past_states.append(current_state)
