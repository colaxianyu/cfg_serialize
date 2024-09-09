from dataclasses import dataclass, field
from typing import List, Generic, TypeVar

@dataclass
class Node:
    id_: int
    asm_code_: List[str] = field(default_factory = list)

@dataclass
class Edge:
    from_node_id_: int
    to_node_id_: int

N = TypeVar('N', bound = Node)
E = TypeVar('E', bound = Edge)

@dataclass
class GraphObject(Generic[N, E]):
    nodes_: List[N] = field(default_factory = list)
    edges_: List[E] = field(default_factory = list)
