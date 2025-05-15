import time
import logging
from abc import ABC, abstractmethod

from ..communication.communicator import Communicator
from ..sts.gamestate.player import PlayerClass
from ..sts.gamestate.received_state import ReceivedState
from ..sts.gamestate.screen_state import ScreenType
from ..sts.constants.events import EventType
from ..logging.logger import STSLogger

class BaseRunner(ABC):
    def __init__(self, communicator: Communicator, logger: STSLogger):
        self.communicator = communicator
        self.past_states = []
        self.logger = logger

    def run(self, player_class: PlayerClass, ascension: int, seed: str):
        self.communicator.send_ready()
        time.sleep(5)
        self.start_game(player_class=player_class, ascension=ascension, seed=seed)
        # state = self.past_states[-1]
        self.climb_spire()


    def start_game(self, player_class: PlayerClass, ascension: int, seed: str):
        self.logger.debug("Starting Game")
        state = self.communicator.start(player_class, ascension, seed)

        success = False
        for _ in range(100):
            if state.game_state.screen_type == ScreenType.MAIN_MENU:
                time.sleep(1)
                state = self.get_current_state()
                self.logger.debug(f"trying to get out of main menu:\n{state}")
            else:
                success = True
                break
        if not success:
            raise TimeoutError("Could not get out of MAIN_MENU after game start.")
        
        assert state.game_state.screen_state.event_id == EventType.NEOW_EVENT
        self.past_states.append(state)

    def get_current_state(self) -> ReceivedState:
        stable = False

        for i in range(100):
            state = self.communicator.current_state()

            if state.ready_for_command:
                stable = True
                break

            time.sleep(0.05)

        if not stable:
            raise RuntimeError("Unable to retrieve a stable observation")
        
        return state

    @abstractmethod
    def climb_spire(self):
        ...

    





