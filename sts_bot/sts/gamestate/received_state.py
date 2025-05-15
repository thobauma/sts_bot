from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from .game_state import GameState


@dataclass
class ReceivedState:
    state_dict: dict[str, Any]
    ready_for_command: bool
    available_commands: Optional[List[str]] = None
    in_game: Optional[bool] = None
    game_state: Optional[GameState] = None
    error: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.game_state, dict):
            self.game_state["class_name"] = self.game_state["class"]
            del self.game_state["class"]
            self.game_state = GameState(**self.game_state)
        if self.available_commands is not None:
            actions = ["choose", "potion", "play", "proceed", "start", "end", "potion"]
            self.valid_commands = list(set(self.available_commands) & set(actions))
