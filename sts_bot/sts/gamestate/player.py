from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum

from .power import Power


class PlayerClass(Enum):
    IRONCLAD = "Ironclad"
    SILENT = "Silent"
    DEFECT = "Defect"
    WATCHER = "Watcher"


@dataclass
class Orb:
    name: str
    id: str
    evoke_amount: int
    passive_amount: int


@dataclass
class Player:
    energy: int
    max_hp: int
    block: int
    orbs: List[Orb] = field(default_factory=list)
    powers: List[Power] = field(default_factory=list)
    current_hp: int = -1

    def __post_init__(self):
        if len(self.powers) > 0 and not isinstance(self.powers[0], Power):
            self.powers = [Power(**c) for c in self.powers]
        if self.current_hp == -1:
            self.current_hp = self.max_hp
        if len(self.orbs) > 0 and not isinstance(self.orbs[0], Orb):
            self.orbs = [Orb(**c) for c in self.orbs]
