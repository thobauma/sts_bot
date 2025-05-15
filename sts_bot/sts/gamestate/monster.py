from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum

from .power import Power


class Intent(Enum):
    ATTACK = 1
    ATTACK_BUFF = 2
    ATTACK_DEBUFF = 3
    ATTACK_DEFEND = 4
    BUFF = 5
    DEBUFF = 6
    STRONG_DEBUFF = 7
    DEBUG = 8
    DEFEND = 9
    DEFEND_DEBUFF = 10
    DEFEND_BUFF = 11
    ESCAPE = 12
    MAGIC = 13
    NONE = 14
    SLEEP = 15
    STUN = 16
    UNKNOWN = 17

    def is_attack(self):
        return self in [
            Intent.ATTACK,
            Intent.ATTACK_BUFF,
            Intent.ATTACK_DEBUFF,
            Intent.ATTACK_DEFEND,
        ]


@dataclass
class Monster:
    is_gone: bool
    move_hits: int
    move_base_damage: int
    half_dead: bool
    move_adjusted_damage: int
    intent: str
    move_id: int
    name: str
    id: str
    max_hp: int
    block: int
    powers: List[Power] = field(default_factory=list)
    current_hp: int = -1
    last_move_id: int = -1
    second_last_move_id: int = -1

    def __post_init__(self, **kwargs):
        if len(self.powers) > 0 and not isinstance(self.powers[0], Power):
            self.powers = [Power(**c) for c in self.powers]
        if self.current_hp == -1:
            self.current_hp = self.max_hp
