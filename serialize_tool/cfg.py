from typing import List, Union
from serialize_tool.graph_object import GraphObject, Node, Edge
import numpy as np

class Cnode(Node):
    def __init__(self, id: int, asm_code: List[str]):
        super().__init__(id, asm_code)

    def to_dict(self) -> dict:
        return {'id': self.id_, 'asmcode': self.asm_code_}

class Cedge(Edge):
    def __init__(self, from_node_id: int, to_node_id: int):
        super().__init__(from_node_id, to_node_id)

    def to_list(self) -> List[int]:
        return [self.from_node_id_, self.to_node_id_]

class CFGFormat(GraphObject[Cnode, Cedge]):
    def __init__(self, nodes: List[Union[Node, Cnode]] = None, edges: List[Union[Edge, Cedge]] = None):
        converted_nodes = self._convert_nodes(nodes) if nodes is not None else None
        converted_edges = self._convert_edges(edges) if edges is not None else None
        super().__init__(converted_nodes, converted_edges)

    def _convert_nodes(self, nodes: List[Union[Node, Cnode]]) -> List[Cnode]:
        return [node if isinstance(node, Cnode) else Cnode(node.id_, node.asm_code_) for node in nodes]

    def _convert_edges(self, edges: List[Union[Edge, Cedge]]) -> List[Cedge]:
        return [edge if isinstance(edge, Cedge) else Cedge(edge.from_node_id_, edge.to_node_id_) for edge in edges]

    def to_dict(self) -> dict:
        return {'cfg': {'nodes': [node.to_dict() for node in self.nodes_], 'edges': [edge.to_list() for edge in self.edges_]}}
    
class CFG:
    def __init__(self, node_list, edge_list) -> None:
        self.cfg_format_ = CFGFormat(node_list, edge_list)
        self.forward_edges_ = dict()
        self.backward_edges_ = dict()
        self.isolated_nodes_ = set()

        self.__set_forward_edges()
        self.__set_backward_edges()
        self.__set_isolated_nodes()
        self.__set_adjacency_list()
        self.root_id_ = self.__find_root_id()
        self.root_node_ = self.find_node_from_id(self.root_id_)

    def __is_empty(self) -> bool:
        return not self.cfg_format_.nodes_ and not self.cfg_format_.edges_        

    def __find_root_id(self) -> int:
        for node in self.cfg_format_.nodes_:
            if node.id_ not in self.forward_edges_ and node.id_ in self.backward_edges_:
                return node.id_
        return None

    def __set_forward_edges(self):
        for edge in self.cfg_format_.edges_:
            self.forward_edges_.setdefault(edge.to_node_id_, []).append(edge.from_node_id_)

    def __set_backward_edges(self):
        for edge in self.cfg_format_.edges_:
            self.backward_edges_.setdefault(edge.from_node_id_, []).append(edge.to_node_id_)
    
    def __set_isolated_nodes(self):
        all_nodes = set(node.id_ for node in self.cfg_format_.nodes_)
        connected_nodes = set(self.forward_edges_.keys()) | set(self.backward_edges_.keys())
        self.isolated_nodes_ = all_nodes - connected_nodes

    def __set_adjacency_list(self) -> None:
        self.adjacency_list_ = {node_id.id_: [] for node_id in self.cfg_format_.nodes_}
        for edge in self.cfg_format_.edges_:
            start_id = edge.from_node_id_
            end_id = edge.to_node_id_
            self.adjacency_list_[start_id].append(end_id)

    def find_node_from_id(self, node_id: int) -> Cnode:
        for node in self.cfg_format_.nodes_:
            if node_id == node.id_:
                return node

    def to_dict(self) -> dict:
        return self.cfg_format.to_dict()