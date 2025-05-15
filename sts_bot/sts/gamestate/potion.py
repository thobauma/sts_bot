from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class Potion:
    requires_target: bool
    can_use: bool
    can_discard: bool
    name: str
    id: str
    price: int = -1

    def __eq__(self, other):
        return other.id == self.id
