from typing import List, Generic, TypeVar

class Node:
    def __init__(self, id: int, asm_code: List[str] = None) -> None:
        self.id_ = id
        self.asm_code_ = asm_code if asm_code is not None else []

class Edge:
    def __init__(self, from_node_id: int, to_node_id: int) -> None:
        self.from_node_id_ = from_node_id
        self.to_node_id_ = to_node_id

N = TypeVar('N', bound = Node)
E = TypeVar('E', bound = Edge)

class GraphObject(Generic[N, E]):
    def __init__(self, nodes: List[N] = None, edges: List[E] = None):
        self.nodes_ = nodes if nodes is not None else []
        self.edges_ = edges if edges is not None else []
