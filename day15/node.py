from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass
class Node:
    coords: Tuple[int, int]
    risk: int
    visited: bool = False
    dist: Optional[int] = None

    def __lt__(self, other):
        return self.dist < other.dist
