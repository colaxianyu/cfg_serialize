from dataclasses import dataclass, field
from typing import List
from serialize_tool.graph_object import GraphObject, Node, Edge

@dataclass
class Cnode(Node):
    def to_dict(self) -> dict:
        return {'id': self.id_, 'asmcode': self.asm_code_}

@dataclass
class Cedge(Edge):
    def to_list(self) -> List[int]:
        return [self.from_node_id_, self.to_node_id_]

@dataclass
class CFGFormat(GraphObject[Cnode, Cedge]):
    def __post_init__(self):
        self.nodes_ = [Cnode(n.id_, n.asm_code_) if isinstance(n, Node) else n for n in self.nodes_]
        self.edges_ = [Cedge(e.from_node_id_, e.to_node_id_) if isinstance(e, Edge) else e for e in self.edges_]

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
        self.root_id_ = self.__find_root_id()

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

    def to_dict(self) -> dict:
        return self.cfg_format.to_dict()