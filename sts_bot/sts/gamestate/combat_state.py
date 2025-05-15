from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .card import Card
from .monster import Monster
from .player import Player
from .deck import CardList


@dataclass
class CombatState:
    draw_pile: CardList
    discard_pile: CardList
    exhaust_pile: CardList
    cards_discarded_this_turn: int
    times_damaged: int
    monsters: List[Monster]
    turn: int
    hand: CardList
    player: Player
    limbo: Optional[CardList]

    def __post_init__(self):
        if isinstance(self.draw_pile, list):
            self.draw_pile = CardList.from_list(self.draw_pile)
        if isinstance(self.discard_pile, list):
            self.discard_pile = CardList.from_list(self.discard_pile)
        if isinstance(self.exhaust_pile, list):
            self.exhaust_pile = CardList.from_list(self.exhaust_pile)
        if isinstance(self.hand, list):
            self.hand = CardList.from_list(self.hand)
        if isinstance(self.limbo, list):
            self.limbo = CardList.from_list(self.limbo)
        if isinstance(self.player, dict):
            self.player = Player(**self.player)
        if (
            isinstance(self.monsters, list)
            and len(self.monsters) > 0
            and isinstance(self.monsters[0], dict)
        ):
            self.monsters = [Monster(**m) for m in self.monsters]

    def to_dict(self):
        d = {"draw_pile": self.draw_pile.to_dict(),
             "discard_pile": self.discard_pile.to_dict(),
             "exhaust_pile": self.exhaust_pile.to_dict(),
             "monsters": self.monsters.to_dict(),
             "hand": self.hand.to_dict()
             "player": self.player.to_dict()}