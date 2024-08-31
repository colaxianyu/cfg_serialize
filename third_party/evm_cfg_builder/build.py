import logging
import os
import sys
from typing import Optional, Union

from crytic_compile import CryticCompile, InvalidCompilation, is_supported

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)

from third_party.evm_cfg_builder.cfg.cfg import CFG
from third_party.evm_cfg_builder.known_hashes.known_hashes import known_hashes

logging.basicConfig()
logger = logging.getLogger("evm-cfg-builder")

def _output_to_dot(d: str, filename: str, cfg: CFG) -> None:
    if not os.path.exists(d):
        os.makedirs(d)
    filename = os.path.basename(filename)
    filename = os.path.join(d, filename + "_")
    cfg.output_to_dot(filename)
    for function in cfg.functions:
        function.output_to_dot(filename)


def _run(bytecode: Optional[Union[str, bytes]], filename: str, dot_directory: Optional[str] = None, disable_optimizations: bool = False, disable_cfg: bool = False) -> None:
    optimization_enabled = not disable_optimizations

    cfg = CFG(bytecode, optimization_enabled=optimization_enabled, compute_cfgs=not disable_cfg)

    for function in cfg.functions:
        logger.info(function)

    if dot_directory:
        _output_to_dot(dot_directory, filename, cfg)


def process_evm_file(filename: str, dot_directory: Optional[str] = None, disable_optimizations: bool = False, disable_cfg: bool = False) -> None:
    if is_supported(filename):
        try:
            cryticCompile = CryticCompile(filename)
            for key, compilation_unit in cryticCompile.compilation_units.items():
                for contract in compilation_unit.contracts_names:
                    bytecode_init = compilation_unit.bytecode_init(contract)
                    if bytecode_init:
                        for signature, hash_id in compilation_unit.hashes(contract).items():
                            known_hashes[hash_id] = signature
                        logger.info(f"Analyze {contract}")
                        _run(bytecode_init, f"{key}-{filename}-{contract}-init", dot_directory, disable_optimizations, disable_cfg)
                        runtime_bytecode = compilation_unit.bytecode_runtime(contract)
                        if runtime_bytecode:
                            _run(runtime_bytecode, f"{key}-{filename}-{contract}-runtime", dot_directory, disable_optimizations, disable_cfg)
                        else:
                            logger.info("Runtime bytecode not available")
        except InvalidCompilation as e:
            logger.error(e)
    else:
        with open(filename, "rb") as f:
            bytecode = f.read()
        logger.info(f"Analyze {filename}")
        _run(bytecode, filename, dot_directory, disable_optimizations, disable_cfg)

