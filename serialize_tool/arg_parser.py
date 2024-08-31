import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CFG Serialization Program")

    parser.add_argument(
        "-i", "--input-dir",
        help="输入DOT文件的目录路径",
        required=True  # 设置为必填项
    )

    parser.add_argument(
        "-o", "--output-dir",
        help="输出序列化文件的目录路径"
    )

    parser.add_argument(
        "-f", "--serialize-format",
        choices=["json", "pkl"],
        default="json",
        help="指定序列化文件的格式，支持json或pkl"
    )

    parser.add_argument(
        "-d", "--delete-dot",
        help="调用evm_cfg_builder生成DOT文件",
        action="store_true"
    )

    return parser.parse_args()