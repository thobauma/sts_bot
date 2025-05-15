from dataclasses import dataclass, field
from typing import List, Dict, Any
from .card import Card, CardType


@dataclass
class CardList:
    cards: List[Card]
    contains_curses: bool
    attack_indices: List[int]
    skill_indices: List[int]
    power_indices: List[int]
    status_indices: List[int]
    curse_indices: List[int]

    @classmethod
    def from_list(cls, l: List[Any]):
        contains_curses = False
        cards = []
        attack_indices = []
        skill_indices = []
        power_indices = []
        status_indices = []
        curse_indices = []

        for i, card_data in enumerate(l):
            card_data["card_type"] = card_data["type"]
            del card_data["type"]
            card = Card(**card_data)
            match card.card_type:
                case CardType.SKILL:
                    skill_indices.append(i)
                case CardType.ATTACK:
                    attack_indices.append(i)
                case CardType.POWER:
                    power_indices.append(i)
                case CardType.STATUS:
                    status_indices.append(i)
                case CardType.CURSE:
                    curse_indices.append(i)
                    contains_curses = True
            cards.append(card)

        return cls(
            cards=cards,
            contains_curses=contains_curses,
            attack_indices=attack_indices,
            skill_indices=skill_indices,
            power_indices=power_indices,
            status_indices=status_indices,
            curse_indices=curse_indices,
        )

    def get_card_index(self, id: str) -> int:
        for i, card in enumerate(self.cards):
            if card.id == id:
                return i
        return -1

    def contains_type(self, type: CardType) -> bool:
        for card in self.cards:
            if card.card_type == type:
                return True
        return False

    def contains_curses_of_any_kind(self) -> bool:
        for card in self.cards:
            if card.card_type == CardType.CURSE:
                return True
        return False


@dataclass
class Deck(CardList):

    def contains_type(self, type: CardType) -> bool:
        for card in self.cards:
            if card.card_type == type:
                return True
        return False

    def contains_curses_of_any_kind(self) -> bool:
        for card in self.cards:
            if card.card_type == CardType.CURSE:
                return True
        return False
