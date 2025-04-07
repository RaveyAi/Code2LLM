import argparse
import cmd
from src.code2llm.services import repo_service
import sys
from pathlib import Path

from src.code2llm.config import VectorDBConfig
from src.code2llm.services import index_service, vector_db_factory

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent  # 根据实际层级调整
sys.path.insert(0, str(project_root))

def do_exit(_):
    """退出程序"""
    print("再见！")
    return True


class Code2LLMShell(cmd.Cmd):
    prompt = "\033[94m(code2llm) \033[0m"


def code_mode(args):
    """代码处理模式"""
    config = VectorDBConfig()
    vectordb = vector_db_factory.get_vector_db(config)

    try:
        # 删除旧数据
        repo_name = args.repo.split("/")[-1].replace(".git", "")
        deleted = vectordb.delete_by_repo(repo_name)
        print(f"已清理旧数据: {deleted}个块")

        # 处理代码库
        processor = repo_service.RepomixProcessor(args.repo)
        # processor.clone_repository()
        md_path = processor.generate_markdown(compress=args.compress)
        markdown_chunker = index_service.MarkdownChunker(200)
        chunks = markdown_chunker.chunk_markdown(md_path, repo_name)

        # 插入向量数据库
        inserted = vectordb.upsert_chunks(chunks)
        print(f"成功处理仓库，插入{inserted}个代码块")

    except Exception as e:
        print(f"处理失败: {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code2LLM - 智能代码分析工具")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Code模式
    code_parser = subparsers.add_parser("code", help="处理代码仓库")
    code_parser.add_argument("--repo", required=True, help="Git仓库URL")
    code_parser.add_argument("--compress", action="store_true", help="启用代码压缩")
    code_parser.set_defaults(func=code_mode)

    args = parser.parse_args()
    args.func(args)
