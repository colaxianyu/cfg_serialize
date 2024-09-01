import os
import json
from serialize_tool.cfg_format import CFGFomat

class CFGUnserialize:
    def __init__(self) -> None:
        self.cfg_ = CFGFomat()

    def __read_json_from_cfg(self, file_path: str) -> None:
        self.cfg_.nodes_.clear()
        self.cfg_.edges_.clear()

        if not os.path.exists(file_path):
            print(f"Path not found: {file_path}")
        
        try:
           with open(file_path, 'r') as f:
               data = json.load(f)
               self.cfg_.edges_ = data['cfg']['edges']
               self.cfg_.nodes_ = data['cfg']['nodes']
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {file_path}: {str(e)}")
    
    def __read_json_from_edges_and_nodes(self, nodes_file: str, edges_file: str) -> None:
        if not os.path.exists(nodes_file) or not os.path.exists(edges_file):
            print(f"Path not found: {nodes_file} or {edges_file}")
            return

        try:
            with open(nodes_file, 'r') as f:
                self.cfg_.nodes_ = json.load(f)
            with open(edges_file, 'r') as f:
                data = json.load(f)
                self.cfg_.edges_ = data['edges']
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {str(e)}")

    def __read_json(self, *file_paths: str) -> None:
        self.cfg_.nodes_.clear()
        self.cfg_.edges_.clear()

        if len(file_paths) == 1:
            self.__read_json_from_cfg(file_paths[0])
        elif len(file_paths) == 2:
            self.__read_json_from_edges_and_nodes(file_paths[0], file_paths[1])

    def get_cfg(self, *file_paths: str) -> CFGFomat:
        self.__read_json(file_paths)
        return self.cfg_