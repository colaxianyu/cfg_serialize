from serialize_tool.cfg_serialize import CFGSerialization
from serialize_tool.arg_parser import parse_args

def serialize_cfgs_ex(input_dir: str, output_dir = None, file_format = 'json', delete_dot = False, is_serialize_graph2vec = False) -> None:
    serializer = CFGSerialization()
    serializer.serialize_cfgs(input_dir, output_dir, file_format, delete_dot, is_serialize_graph2vec)

def main():
    args = parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    file_format = args.file_format
    delete_dot = args.delete_dot
    is_serialize_graph2vec = args.serialize_graph2vec

    serialize_cfgs_ex(input_dir, output_dir, file_format, delete_dot, is_serialize_graph2vec)


if __name__ == "__main__":
    main()