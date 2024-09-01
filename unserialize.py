from serialize_tool.cfg_format import CFGFomat
from serialize_tool.cfg_unserialize import CFGUnserialize

def unserialize_cfgs_ex(*file_paths: str) -> CFGFomat:
    unserialize = CFGUnserialize();
    return unserialize.get_cfg(file_paths)
