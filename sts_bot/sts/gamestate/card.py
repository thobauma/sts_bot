from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional


class CardType(Enum):
    SKILL = "SKILL"
    ATTACK = "ATTACK"
    POWER = "POWER"
    STATUS = "STATUS"
    CURSE = "CURSE"
    FAKE = "FAKE"
    OTHER = "OTHER"


class CardRarity(Enum):
    BASIC = "BASIC"
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    SPECIAL = "SPECIAL"
    CURSE = "CURSE"


@dataclass
class Card:
    exhausts: bool
    cost: int
    name: str
    id: str
    card_type: CardType
    ethereal: bool
    uuid: str
    upgrades: int
    rarity: CardRarity
    has_target: bool
    is_playable: Optional[bool] = None
    price: Optional[int] = -1
    misc: Optional[int] = -1

    def __post_init__(self):
        if not isinstance(self.card_type, CardType):
            self.card_type = CardType(self.card_type)
        if not isinstance(self.rarity, CardRarity):
            self.rarity = CardRarity(self.rarity)

    def __eq__(self, other):
        return self.uuid == other.uuid

    def to_dict(self):
        d = {"exhausts": self.exhausts,
             "cost": }
    # def prompt_format(self):
    #     return asdict(self)

