import os
import json
from serialize_tool.cfg_format import CFGFomat

class CFGUnserialize:
    def __init__(self) -> None:
        self.cfg_ = CFGFomat()

    def __read_json(self, file_path: str) -> None:
        self.cfg_.nodes_.clear()
        self.cfg_.edges_.clear()

        if not os.path.exists(file_path):
            print(f"Path not found: {file_path}")
        
        try:
           with open(file_path, 'r') as f:
               data = json.load(f)
               self.cfg_ = data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file {file_path}: {str(e)}")
    
    def get_cfg(self, file_path: str) -> CFGFomat:
        self.__read_json(file_path)
        return self.cfg_