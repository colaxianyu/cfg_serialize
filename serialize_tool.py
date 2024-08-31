from serialize_tool.cfg_serialize import CFGSerialization
from serialize_tool.arg_parser import parse_args

def serialize_cfgs_ex(input_dir: str, output_dir = None, file_format = 'json', delete_dot = False) -> None:
    serializer = CFGSerialization()
    serializer.serialize_cfgs(input_dir, output_dir, file_format, delete_dot)

def main():
    args = parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    file_format = args.file_format
    delete_dot = args.delete_dot

    serialize_cfgs_ex(input_dir, output_dir, file_format, delete_dot)


if __name__ == "__main__":
    main()