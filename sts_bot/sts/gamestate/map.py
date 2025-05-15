from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum


class MapSymbol(Enum):
    ENEMY = "M"
    UNKNOWN = "?"
    SHOP = "$"
    REST = "R"
    TREASURE = "T"
    ELITE = "E"
    START = "S"


@dataclass
class MapNode:
    x: int
    y: int
    symbol: MapSymbol = MapSymbol.START
    children: List[MapNode] = field(default_factory=list)
    parents: List[Any] = field(default_factory=list)

    def __post_init__(self):
        if len(self.children) > 0 and not isinstance(self.children[0], MapNode):
            self.children = [MapNode(**c) for c in self.children]

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Map:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        if node.y in self.nodes:
            self.nodes[node.y][node.x] = node
        else:
            self.nodes[node.y] = {node.x: node}

    def get_node(self, x, y) -> MapNode:
        if y in self.nodes and x in self.nodes[y]:
            return self.nodes[y][x]
        else:
            return None

    @classmethod
    def from_list(cls, node_list):
        dungeon_map = Map()
        for n in node_list:
            node = MapNode(**n)
            dungeon_map.add_node(node)

        for n in node_list:
            children = n.get("children")
            parent_node = dungeon_map.get_node(n.get("x"), n.get("y"))
            for child in children:
                child_node = dungeon_map.get_node(child.get("x"), child.get("y"))
                if child_node is not None:
                    parent_node.children.append(child_node)

        return dungeon_map
