from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .combat_state import CombatState
from .card import Card
from .deck import CardList
from .relic import Relic
from .potion import Potion
from .screen_state import Screen, screen_from_dict, ScreenType
from .map import Map

@dataclass
class GameState:
    screen_type: ScreenType
    seed: int
    deck: CardList
    relics: List[Relic]
    max_hp: int
    act_boss: str
    gold: int
    action_phase: str
    act: int
    screen_name: str
    room_phase: str
    is_screen_up: bool
    potions: List[Potion]
    current_hp: int
    floor: int
    ascension_level: int
    class_name: str  # "class" is a reserved keyword in Python
    room_type: str
    map: Optional[Map] = None
    combat_state: Optional[CombatState] = None
    screen_state: Optional[Screen] = None
    choice_list: Optional[List[str]] = None

    def __post_init__(self):
        if isinstance(self.screen_type, str):
            self.screen_type = ScreenType[self.screen_type]
        if isinstance(self.screen_state, dict):
            self.screen_state = screen_from_dict(self.screen_type, self.screen_state)
        if isinstance(self.combat_state, dict):
            self.combat_state = CombatState(**self.combat_state)
        if len(self.potions) > 0:
            self.potions = [Potion(**p) for p in self.potions]
        if len(self.relics) > 0:
            self.relics = [Relic(**r) for r in self.relics]
        if isinstance(self.deck, list):
            self.deck = CardList.from_list(self.deck)
        if isinstance(self.map, list):
            self.map = Map.from_list(self.map)

