from dataclasses import dataclass, field
from typing import List

@dataclass
class Node:
    id_: int
    asm_code_: List[str] = field(default_factory = list)

    def to_dict(self) -> dict:
        return {'id': self.id_, 'asmcode': self.asm_code_}

@dataclass
class Edge:
    from_node_id_: int
    to_node_id_: int

    def to_list(self) -> List[int]:
        return [self.from_node_id_, self.to_node_id_]

@dataclass
class CFGFomat:
    nodes_: List[Node] = field(default_factory = list)
    edges_: List[Edge] = field(default_factory = list)

    def to_dict(self) -> dict:
        return {'cfg': {'nodes': [node.to_dict() for node in self.nodes_], 'edges': [edge.to_list() for edge in self.edges_]}}