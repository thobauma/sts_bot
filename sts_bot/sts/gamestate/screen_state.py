from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


from .card import Card
from .deck import CardList
from .relic import Relic
from .potion import Potion
from .map import MapNode
from sts_bot.sts.constants.events import EventType

class ScreenType(Enum):
    EVENT = 1
    CHEST = 2
    SHOP_ROOM = 3
    REST = 4
    CARD_REWARD = 5
    COMBAT_REWARD = 6
    MAP = 7
    BOSS_REWARD = 8
    SHOP_SCREEN = 9
    GRID = 10
    HAND_SELECT = 11
    GAME_OVER = 12
    COMPLETE = 13
    NONE = 14
    MAIN_MENU = 15


class ChestType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    BOSS = 4
    UNKNOWN = 5


class RewardType(Enum):
    CARD = 1
    GOLD = 2
    RELIC = 3
    POTION = 4
    STOLEN_GOLD = 5
    EMERALD_KEY = 6
    SAPPHIRE_KEY = 7


class RestOption(Enum):
    DIG = 1
    LIFT = 2
    RECALL = 3
    REST = 4
    SMITH = 5
    TOKE = 6


@dataclass
class EventOption:
    text: str
    label: str
    disabled: bool = False
    choice_index: Optional[int] = None


class Screen:

    SCREEN_TYPE = ScreenType.NONE

    def __init__(self):
        self.screen_type = type(self).SCREEN_TYPE

    @classmethod
    def from_dict(cls, d):
        return cls()


class ChestScreen(Screen):

    SCREEN_TYPE = ScreenType.CHEST

    def __init__(self, chest_type, chest_open):
        super().__init__()
        self.chest_type = chest_type
        self.chest_open = chest_open

    @classmethod
    def from_dict(cls, state_dict):
        java_chest_class_name = state_dict.get("chest_type")
        if java_chest_class_name == "SmallChest":
            chest_type = ChestType.SMALL
        elif java_chest_class_name == "MediumChest":
            chest_type = ChestType.MEDIUM
        elif java_chest_class_name == "LargeChest":
            chest_type = ChestType.LARGE
        elif java_chest_class_name == "BossChest":
            chest_type = ChestType.BOSS
        else:
            chest_type = ChestType.UNKNOWN
        chest_open = state_dict.get("chest_open")
        return cls(chest_type, chest_open)


class EventScreen(Screen):

    SCREEN_TYPE = ScreenType.EVENT

    def __init__(self, name, event_id, body_text=""):
        super().__init__()
        self.event_name = name
        self.event_id = EventType(event_id)
        self.body_text = body_text
        self.options = []

    @classmethod
    def from_dict(cls, state_dict):
        event = cls(
            state_dict["event_name"], state_dict["event_id"], state_dict["body_text"]
        )
        for option in state_dict["options"]:
            event.options.append(EventOption(**option))
        return event


class ShopRoomScreen(Screen):

    SCREEN_TYPE = ScreenType.SHOP_ROOM


class RestScreen(Screen):

    SCREEN_TYPE = ScreenType.REST

    def __init__(self, has_rested, rest_options):
        super().__init__()
        self.has_rested = has_rested
        self.rest_options = rest_options

    @classmethod
    def from_dict(cls, state_dict):
        rest_options = [
            RestOption[option.upper()] for option in state_dict.get("rest_options")
        ]
        return cls(state_dict.get("has_rested"), rest_options)


class CardRewardScreen(Screen):

    SCREEN_TYPE = ScreenType.CARD_REWARD

    def __init__(self, cards, can_bowl, can_skip):
        super().__init__()
        self.cards = cards
        self.can_bowl = can_bowl
        self.can_skip = can_skip

    @classmethod
    def from_dict(cls, state_dict):
        cards = CardList.from_list(state_dict.get("cards"))
        can_bowl = state_dict.get("bowl_available")
        can_skip = state_dict.get("skip_available")
        return cls(cards, can_bowl, can_skip)


@dataclass
class CombatReward:
    reward_type: RewardType
    gold: Optional[int] = None
    relic: Optional[Relic] = None
    potion: Optional[Potion] = None
    link: Optional[Relic] = None

    def __eq__(self, other):
        return (
            self.reward_type == other.reward_type
            and self.gold == other.gold
            and self.relic == other.relic
            and self.potion == other.potion
            and self.link == other.link
        )


class CombatRewardScreen(Screen):

    SCREEN_TYPE = ScreenType.COMBAT_REWARD

    def __init__(self, rewards):
        super().__init__()
        self.rewards = rewards

    @classmethod
    def from_dict(cls, state_dict):
        rewards = []
        for reward_ in state_dict.get("rewards"):
            reward_type = RewardType[reward_.get("reward_type")]
            if reward_type in [RewardType.GOLD, RewardType.STOLEN_GOLD]:
                rewards.append(CombatReward(reward_type, gold=reward_.get("gold")))
            elif reward_type == RewardType.RELIC:
                rewards.append(
                    CombatReward(reward_type, relic=Relic(**reward_.get("relic")))
                )
            elif reward_type == RewardType.POTION:
                rewards.append(
                    CombatReward(reward_type, potion=Potion(**reward_.get("potion")))
                )
            elif reward_type == RewardType.SAPPHIRE_KEY:
                rewards.append(
                    CombatReward(reward_type, link=Relic(**reward_.get("link")))
                )
            else:
                rewards.append(CombatReward(reward_type))
        return cls(rewards)


class MapScreen(Screen):

    SCREEN_TYPE = ScreenType.MAP

    def __init__(self, current_node, next_nodes, boss_available):
        super().__init__()
        self.current_node = current_node
        self.next_nodes = next_nodes
        self.boss_available = boss_available

    @classmethod
    def from_dict(cls, state_dict):
        current_node_ = state_dict.get("current_node", None)
        next_nodes_ = state_dict.get("next_nodes", None)
        boss_available = state_dict.get("boss_available")
        if current_node_ is not None:
            current_node = MapNode(**current_node_)
        else:
            current_node = None
        if next_nodes_ is not None:
            next_nodes = [MapNode(**node) for node in next_nodes_]
        else:
            next_nodes = []
        return cls(current_node, next_nodes, boss_available)


class BossRewardScreen(Screen):

    SCREEN_TYPE = ScreenType.BOSS_REWARD

    def __init__(self, relics):
        super().__init__()
        self.relics = relics

    @classmethod
    def from_dict(cls, state_dict):
        relics = [Relic(**relic) for relic in state_dict.get("relics")]
        return cls(relics)


class ShopScreen(Screen):

    SCREEN_TYPE = ScreenType.SHOP_SCREEN

    def __init__(self, cards, relics, potions, purge_available, purge_cost):
        super().__init__()
        self.cards = cards
        self.relics = relics
        self.potions = potions
        self.purge_available = purge_available
        self.purge_cost = purge_cost

    @classmethod
    def from_dict(cls, state_dict):
        # cards = [Card(**card) for card in state_dict.get("cards")]
        cards = CardList.from_list(state_dict.get("cards"))
        relics = [Relic(**relic) for relic in state_dict.get("relics")]
        potions = [Potion(**potion) for potion in state_dict.get("potions")]
        purge_available = state_dict.get("purge_available")
        purge_cost = state_dict.get("purge_cost")
        return cls(cards, relics, potions, purge_available, purge_cost)


class GridSelectScreen(Screen):

    SCREEN_TYPE = ScreenType.GRID

    def __init__(
        self,
        cards,
        selected_cards,
        num_cards,
        any_number,
        confirm_up,
        for_upgrade,
        for_transform,
        for_purge,
    ):
        super().__init__()
        self.cards = cards
        self.selected_cards = selected_cards
        self.num_cards = num_cards
        self.any_number = any_number
        self.confirm_up = confirm_up
        self.for_upgrade = for_upgrade
        self.for_transform = for_transform
        self.for_purge = for_purge

    @classmethod
    def from_dict(cls, state_dict):
        # cards = [Card(**card) for card in state_dict.get("cards")]
        # selected_cards = [Card(**card) for card in state_dict.get("selected_cards")]
        cards = CardList.from_list(state_dict.get("cards"))
        selected_cards = CardList.from_list(state_dict.get("selected_cards"))
        num_cards = state_dict.get("num_cards")
        any_number = state_dict.get("any_number", False)
        confirm_up = state_dict.get("confirm_up")
        for_upgrade = state_dict.get("for_upgrade")
        for_transform = state_dict.get("for_transform")
        for_purge = state_dict.get("for_purge")
        return cls(
            cards,
            selected_cards,
            num_cards,
            any_number,
            confirm_up,
            for_upgrade,
            for_transform,
            for_purge,
        )


class HandSelectScreen(Screen):

    SCREEN_TYPE = ScreenType.HAND_SELECT

    def __init__(self, cards, selected, num_cards, can_pick_zero):
        super().__init__()
        self.cards = cards
        self.selected_cards = selected
        self.num_cards = num_cards
        self.can_pick_zero = can_pick_zero

    @classmethod
    def from_dict(cls, state_dict):
        # cards = [Card(**card) for card in state_dict.get("hand")]
        # selected_cards = [Card(**card) for card in state_dict.get("selected")]
        cards = CardList.from_list(state_dict.get("cards"))
        selected_cards = CardList.from_list(state_dict.get("selected_cards"))
        num_cards = state_dict.get("max_cards")
        can_pick_zero = state_dict.get("can_pick_zero")
        return cls(cards, selected_cards, num_cards, can_pick_zero)


class GameOverScreen(Screen):

    SCREEN_TYPE = ScreenType.GAME_OVER

    def __init__(self, score, victory):
        super().__init__()
        self.score = score
        self.victory = victory

    @classmethod
    def from_dict(cls, state_dict):
        return cls(state_dict.get("score"), state_dict.get("victory"))


class CompleteScreen(Screen):

    SCREEN_TYPE = ScreenType.COMPLETE


SCREEN_CLASSES = {
    ScreenType.EVENT: EventScreen,
    ScreenType.CHEST: ChestScreen,
    ScreenType.SHOP_ROOM: ShopRoomScreen,
    ScreenType.REST: RestScreen,
    ScreenType.CARD_REWARD: CardRewardScreen,
    ScreenType.COMBAT_REWARD: CombatRewardScreen,
    ScreenType.MAP: MapScreen,
    ScreenType.BOSS_REWARD: BossRewardScreen,
    ScreenType.SHOP_SCREEN: ShopScreen,
    ScreenType.GRID: GridSelectScreen,
    ScreenType.HAND_SELECT: HandSelectScreen,
    ScreenType.GAME_OVER: GameOverScreen,
    ScreenType.COMPLETE: CompleteScreen,
    ScreenType.NONE: Screen,
}


def screen_from_dict(screen_type, state_dict):
    return SCREEN_CLASSES[screen_type].from_dict(state_dict)
