from serialize_tool.cfg_format import CFGFomat
from serialize_tool.cfg_unserialize import CFGUnserialize

def unserialize_cfgs_ex(*file_paths: str) -> CFGFomat:
    unserialize = CFGUnserialize();
    return unserialize.get_cfg(*file_paths)


input_nodes = "D:\\MyFile\\Download\\evm_cfg_builder\\results\\recurse\\result_json\\Nodes_json\\nodes_recurse.evm__dispatcher.json"
input_edges = "D:\\MyFile\\Download\\evm_cfg_builder\\results\\recurse\\result_json\\Edges_json\\edges_recurse.evm__dispatcher.json"
c = unserialize_cfgs_ex(input_nodes, input_edges)
print("123")