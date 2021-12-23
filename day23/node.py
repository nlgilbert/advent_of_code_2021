from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union
    
@dataclass
class Node:
    burrow: List[str]
    energy: int

    def __lt__(self, other: Node):
        return self.energy < other.energy