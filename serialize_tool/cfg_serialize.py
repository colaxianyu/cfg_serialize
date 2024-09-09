import pydot
import json
import pickle
import os
import networkx as nx
from typing import List
from cfg_format import CFG, Node, Edge
from third_party.evm_cfg_builder.build import process_evm_file



class CFGSerialization:
    def __init__(self) -> None:
        self.dot_graphs_ = None
        self.cfg_ = None

    def __unload_cfg(self) -> None:
        if self.cfg_ is None or not self.cfg_.__is_empty():
            self.cfg_ = None

    def __cfg_build(self, input_dir: str, output_dir: str) -> None:    
        self.__unload_cfg()

        for file_name in os.listdir(input_dir):
            if file_name.endswith('.evm'):
                evm_bytecode_file = os.path.join(input_dir, file_name)
                dot_sub_dir = os.path.join(output_dir, os.path.splitext(file_name)[0], 'dot')
                process_evm_file(evm_bytecode_file, dot_directory = dot_sub_dir)

    def __parse_graph(self) -> None:
        first_dot_graph = self.dot_graphs_[0]
        graph = nx.nx_pydot.from_pydot(first_dot_graph)

        nodes = []
        edges = []
        for node_id, attrs in graph.nodes(data = True):
            asm_code_raw = attrs.get('label', '').strip('"')
            asm_code_list = asm_code_raw.split('\n')
            asm_code = [line.split(':', 1)[1].strip() for line in asm_code_list if ':' in line]
            nodes.append(Node(id_ = int(node_id), asm_code_ = asm_code))

        for from_node, to_node in graph.edges():
            edges.append(Edge(from_node_id_ = int(from_node), to_node_id_ = int(to_node)))

        self.cfg_ = CFG(nodes, edges)

    def __serialization(self, file_name, serialize_format, save_path = None, is_serialize_graph2vec = False) -> None:
        if is_serialize_graph2vec:
            nodes_dir = os.path.join(save_path, 'Nodes_json')
            edges_dir = os.path.join(save_path, 'Edges_json')
            os.makedirs(nodes_dir, exist_ok = True)
            os.makedirs(edges_dir, exist_ok = True)

            nodes_file = os.path.join(nodes_dir, f"nodes_{file_name}")
            with open(nodes_file, 'w') as f:
                json.dump([node.to_dict() for node in self.cfg_.cfg_format_.nodes_], f, indent = 2)

            edges_file = os.path.join(edges_dir, f"edges_{file_name}")
            with open(edges_file, 'w') as f:
                json.dump({"edges": [edge.to_list() for edge in self.cfg_.cfg_format_.edges_]}, f, indent = 2)

        else:
            full_save_path = os.path.join(save_path, file_name)
            try:
                if serialize_format == 'json':
                    with open(full_save_path, 'w') as f:
                        json.dump(self.cfg_.to_dict(), f, indent = 2)
                elif serialize_format == 'pkl':
                    with open(full_save_path, 'wb') as f:
                        pickle.dump(self.cfg_, f)
            except Exception as e:
                print(f'Error saving file: {file_name}: {e}')

    def serialize_cfgs(self, input_dir: str, output_dir = None, serialize_format = 'json', delete_dot = False, is_serialize_graph2vec = False) -> None: 
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), 'results')
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.__cfg_build(input_dir, output_dir)
        
        for folder_name in os.listdir(output_dir):
            dot_dir = os.path.join(output_dir, folder_name, 'dot')
            result_dir = os.path.join(output_dir, folder_name, f'result_{serialize_format}')
            if not os.path.exists(result_dir):
                os.makedirs(result_dir)

            for file_name in os.listdir(dot_dir):
                if file_name.endswith('.dot'):
                    dot_file_path = os.path.join(dot_dir, file_name)
                    self.dot_graphs_ = pydot.graph_from_dot_file(dot_file_path)
                    self.__parse_graph()
                    serialize_file_name = file_name.replace('.dot', f'.{serialize_format}')
                    self.__serialization(serialize_file_name, serialize_format, result_dir, is_serialize_graph2vec)

            if delete_dot:
                import shutil
                shutil.rmtree(dot_dir)

# dir = "D:/MyFile/Download/evm_cfg_builder/test1"
# c = CFGSerialization()
# c.serialize_cfgs(dir, is_serialize_graph2vec=True)