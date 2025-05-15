from typing import List, Callable, Any, Optional

import json
import re
from ollama import Client

from .base.base_tool import Tool
from .base.memory import AgentMemory
from .prompts.prompt_generator import PromptGenerator


from sts_bot.sts.gamestate.received_state import ReceivedState
from sts_bot.sts.gamestate.combat_state import CombatState
from sts_bot.sts.gamestate.screen_state import ScreenType
from sts_bot.sts.constants.events import EventType
from sts_bot.logging.logger import STSLogger


class Agent:
    def __init__(
        self,
        client: Client,
        model: str,
        # prompt_file_names: list[str] = ["neow_event", "combat", "shop"],
        logger: STSLogger,
        tools: list[Tool] = [],
        # memory: AgentMemory
    ):
        self.tools = tools
        self.client = client
        self.model = model
        self.prompt_generator = PromptGenerator()
        self.memory = AgentMemory()
        self.logger = logger

    def get_prompt(self):
        pass

    def get_next_action(self, state: ReceivedState):
        game_state = state.game_state
        self.state_dict = state.state_dict
        self.valid_commands = state.valid_commands
        self.game_state = game_state
        return self._screen_type_handler()

    def _screen_type_handler(self) -> Callable | str:
        screen_type = self.game_state.screen_type
        match screen_type:
            case ScreenType.EVENT:
                # Handle event screen
                if len(self.game_state.screen_state.options) == 1:
                    return "choose 0"
                # return self._event_type_handler(screen_type.event_id)
                return self.general_call_handler()

            case ScreenType.CHEST:
                # Handle chest screen
                # TODO handle case with cursed key
                return self.general_call_handler()
            case ScreenType.SHOP_ROOM:
                # Handle shop room (before actual shop screen)
                return "choose 0"
            case ScreenType.REST:
                # Handle campfire/rest screen
                return self.general_call_handler()
            case ScreenType.CARD_REWARD:
                # Handle card reward screen
                # TODO
                return self.general_call_handler()
            case ScreenType.COMBAT_REWARD:
                # Handle combat reward screen
                if len(self.game_state.screen_name.rewards) == 0:
                    return "proceed"
                # return "choose 0"
                return self.general_call_handler("card_reward_options")
            case ScreenType.MAP:
                # Handle map screen
                if len(self.game_state.choice_list) == 1:
                    return "choose 0"
                return self.general_call_handler()
            case ScreenType.BOSS_REWARD:
                # Handle boss reward screen
                return self.general_call_handler()
            case ScreenType.SHOP_SCREEN:
                # Handle actual shop screen
                return self.general_call_handler("shop_options")
            case ScreenType.GRID:
                # Handle grid selection screen
                if "confirm" in self.valid_commands:
                    return "confirm"
                return self.general_call_handler()
            case ScreenType.HAND_SELECT:
                # TODO
                # Handle hand selection screen
                return self.general_call_handler()
            case ScreenType.GAME_OVER:
                # TODO
                # Handle game over screen
                return "choose 0"
            case ScreenType.COMPLETE:
                # TODO
                # Handle run complete screen
                return "choose 0"
            case ScreenType.NONE:
                # TODO
                # Handle undefined
                # screen probably combat
                if isinstance(self.game_state.combat_state, CombatState):
                    return self.combat_call_handler()
                return "choose 0"
            case ScreenType.MAIN_MENU:
                # TODO
                # Handle main menu screen
                return "choose 0"
            case _:
                # Handle unexpected values
                raise ValueError(f"Unknown screen type: {screen_type}")

    # def _event_type_handler(self, event_id) -> Callable | str:
    #     match event_id:
    #         case EventType.NEOW_EVENT:
    #             self._handle_neow_event()
    #         case _:
    #             return "choose 0"

    # def _handle_neow_event(self):
    #     self.game_state

    #     self.call_agent(messages)


    def parse_combat_state(self, combat_state: CombatState):
        player = combat_state.player
        monsters = combat_state.monsters
        hand = combat_state.hand

        state_json = 


    def combat_call_handler(self):
        available_actions = str(self.valid_commands)
        state = self.parse_combat_state(self.game_state.combat_state)
        return self.general_call_handler(
            "combat_examples", "combat_prompt", available_actions=available_actions, game_state=state
        )

    def find_action(self, message):
        message_no_think = message[message.find("</think>") :]
        match = re.search(r"\{([^}]*)\}", message_no_think)
        action_string = match.group(1) if match else "None"

        return action_string

    def general_call_handler(
        self,
        example_key: str = "basic_examples",
        dynamic_key: str = "basic_prompt",
        available_actions: Optional[str | list[str]] = None,
        game_state: Optional[dict[str, Any]] = None,
    ):
        if available_actions is None:
            available_actions = self.valid_commands
        if game_state is None:
            game_state = self.state_dict
        messages = self.prompt_generator.create_prompt(
            game_state=game_state,
            available_actions=available_actions,
            dynamic_key=dynamic_key,
            example_key=example_key,
            logger=self.logger,
            # dynamic_prompt=,
        )
        message = self.call_agent(messages=messages)
        action = self.find_action(message)
        return action

    def call_agent(self, messages, stream=True, keep_alive=-1):
        message = ""
        for part in self.client.chat(
            model=self.model, messages=messages, stream=stream, keep_alive=keep_alive
        ):
            partialmessage = part["message"]["content"]
            message += partialmessage
            print(partialmessage, end="", flush=True)

        return message
