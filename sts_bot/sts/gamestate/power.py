from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .card import Card


@dataclass
class Power:
    id: str
    name: str
    amount: int
    misc: Optional[int] = None
    damage: Optional[int] = None
    just_applied: Optional[bool] = None
    card: Optional[Card] = None

    def __eq__(self, other):
        return self.id == other.id and self.amount == other.amount
