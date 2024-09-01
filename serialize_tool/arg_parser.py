import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CFG Serialization Program")

    parser.add_argument(
        "-i", "--input-dir",
        help = "输入.evm文件的目录路径",
        required = True  
    )

    parser.add_argument(
        "-o", "--output-dir",
        help = "输出序列化文件的目录路径"
    )

    parser.add_argument(
        "-f", "--serialize-format",
        choices = ["json", "pkl"],
        default = "json",
        help = "指定序列化文件的格式，支持json或pkl"
    )

    parser.add_argument(
        "-d", "--delete-dot",
        help = "删除.dot中间文件",
        action = "store_true"
    )

    parser.add_argument(
        "-g", "--serialize-graph2vec",
        help = "分别序列化Node和Edge，使Edge格式符合graph2vec",
        action= "store_true" 
    )

    return parser.parse_args()